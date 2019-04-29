import os
import argparse
import time
import numpy as np
import cv2
import torch
import torch.nn as nn
from torch.autograd import Variable
from models import FFDNet
from utils import batch_psnr, normalize, init_logger_ipol, \
				variable_to_cv2_image, remove_dataparallel_wrapper, is_rgb

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def test_ffdnet(input, cuda, noise_sigma):

        """Denoises an input image with FFDNet
        """
        # Normalize the nose sigma [0, 1] 
        noise_sigma /= 255.
        # Check if input exists and if it is RGB
        rgb_den = is_rgb(input)
        if rgb_den:
            in_ch = 3
            model_fn = '../models/net_rgb.pth'
            imorig = input
            # from HxWxC to CxHxW, RGB image
            imorig = (cv2.cvtColor(imorig, cv2.COLOR_BGR2RGB)).transpose(2, 0, 1)
        else:
            # from HxWxC to  CxHxW grayscale image (C=1)
            in_ch = 1
            model_fn = '../models/net_gray.pth'
            imorig = input
            imorig = np.expand_dims(imorig, 0)
        imorig = np.expand_dims(imorig, 0)
        # Handle odd sizes
        expanded_h = False
        expanded_w = False
        sh_im = imorig.shape
        if sh_im[2]%2 == 1:
            expanded_h = True
            imorig = np.concatenate((imorig, \
                    imorig[:, :, -1, :][:, :, np.newaxis, :]), axis=2)

        if sh_im[3]%2 == 1:
            expanded_w = True
            imorig = np.concatenate((imorig, \
                    imorig[:, :, :, -1][:, :, :, np.newaxis]), axis=3)

        imorig = normalize(imorig)
        imorig = torch.Tensor(imorig)

        # Absolute path to model file
        model_fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), \
                    model_fn)

        # Create model
        net = FFDNet(num_input_channels=in_ch, test_mode=True)

        # Load saved weights
        if cuda:
            state_dict = torch.load(model_fn)
            device_ids = [0]
            model = nn.DataParallel(net, device_ids=device_ids).cuda()
        else:
            state_dict = torch.load(model_fn, map_location='cpu')
            # CPU mode: remove the DataParallel wrapper
            state_dict = remove_dataparallel_wrapper(state_dict)
            model = net
        model.load_state_dict(state_dict)
        # Sets the model in evaluation mode (e.g. it removes BN)
        model.eval()

        # Sets data type according to CPU or GPU modes
        if cuda:
            dtype = torch.cuda.FloatTensor
        else:
            dtype = torch.FloatTensor

        with torch.no_grad():
            imorig = Variable(imorig.type(dtype), volatile=True)
            nsigma = Variable(torch.FloatTensor([noise_sigma]).type(dtype), volatile=True)

        # Estimate noise and subtract it to the input image
        im_noise_estim = model(imorig, nsigma)
        outim = torch.clamp(imorig-im_noise_estim, 0., 1.)

        if expanded_h:
            imorig = imorig[:, :, :-1, :]
            outim = outim[:, :, :-1, :]
            imorig = imorig[:, :, :-1, :]

        if expanded_w:
            imorig = imorig[:, :, :, :-1]
            outim = outim[:, :, :, :-1]
            imorig = imorig[:, :, :, :-1]


        # Save output
        outimg = variable_to_cv2_image(outim)
        return (outimg)
        
    
if __name__ == "__main__":
    imorig = cv2.imread('woman.png')
    outimg = test_ffdnet (imorig, False, 70)
    cv2.imwrite("ffdnet_out.png", outimg)