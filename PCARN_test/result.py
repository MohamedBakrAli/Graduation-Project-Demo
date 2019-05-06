#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 21:32:04 2019

@author: marwan
"""
import os
from collections import OrderedDict
import torch
from .pcarn import Net 
import skimage.io as io
import torchvision.transforms as transforms
import cv2
import torchvision.utils as utils

def compute_image(LR_path,scale, SR_path):
    ckpt_path = '../models/PCARN-L1.pth'
    # Absolute path to model file
    ckpt_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ckpt_path)
    lr = io.imread(LR_path)
    transform = transforms.Compose([
            transforms.ToTensor()
        ])
    lr = transform(lr)
    lr = lr.unsqueeze(0)
    kwargs = {
        "num_channels": 64,
        "groups": 1,
        "mobile": False,
        "scale": scale,
    }
    net = Net(**kwargs).to("cpu")
    state_dict = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k
        # name = k[7:] # remove "module."
        new_state_dict[name] = v
    net.load_state_dict(new_state_dict)
    with torch.no_grad():
        SR = net(lr,scale).detach()
        
        
    utils.save_image(SR.squeeze(0), SR_path)

def main():

    compute_image("/home/bakr/Downloads/test_PCARN/low.jpg",2)

    

if __name__ == "__main__":
    main()

