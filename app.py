
import os
import matplotlib.image as mpimg
import cv2
import matplotlib.pyplot as plt

from FFDNET_test.test_ffdnet_ipol import test_ffdnet
from flask import Flask, request, redirect, url_for, render_template

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# the system has GPU or not
cuda = False


@app.route('/project')
def index ():
    return render_template("project.html")



@app.route('/demo', methods=['GET', 'POST'])
def demo ():
    if request.method == 'GET':
        
        return render_template("demo.html")
    elif request.method == 'POST':
        target = os.path.join(APP_ROOT, 'input')
        if not os.path.isdir(target):
            os.mkdir(target)
        
        # save the input image
        file = request.files.getlist("inputImage")[0]
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
        
       
        print("# : " , request.values)

        # run model Super resolution.
        

        # run models denoising if choice.
        img=mpimg.imread(file)
        outimg = test_ffdnet (img, cuda, 70)
        
        #plt.imshow(outimg)
        #plt.show()
        return outimg



if __name__ == "__main__":
  
    app.run(debug=True)