import os, time
import matplotlib.image as mpimg
import cv2
import matplotlib.pyplot as plt
import torchvision.utils as utils

from flask import Flask, request, redirect, url_for, render_template, send_file
from FFDNET_test.test_ffdnet_ipol import test_ffdnet
from PCARN_test.result import compute_image
from apscheduler.scheduler import Scheduler

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()


def delete_files_every_x_days(path, days):
    now = time.time()
    for filename in os.listdir(path):
        # if os.stat(os.path.join(path, filename)).st_mtime < now - 7 * 86400:
        if os.path.getmtime(os.path.join(path, filename)) < now - 7 * 86400:
            if os.path.isfile(os.path.join(path, filename)):
                print(filename)
                os.remove(os.path.join(path, filename))



@cron.interval_schedule(hours = 4)
def delete_temporary_files():
    input_path = os.path.join(APP_ROOT, 'static/input')
    output_path = os.path.join(APP_ROOT, 'static/output')
    delete_files_every_x_days(input_path, 1)
    delete_files_every_x_days(output_path, 1)



# the system has GPU or not
cuda = False


@app.route('/project')
def index ():
    return render_template("project.html")



@app.route('/demo', methods=['GET'])
def demo ():
    return render_template("demo.html")


@app.route('/demo/result', methods=['POST'])
def result ():
    user_adr = str(request.remote_addr)  + "_"
    target_in = os.path.join(APP_ROOT, 'static/input')
    if not os.path.isdir(target_in):
        os.mkdir(target_in)


    target_out = os.path.join(APP_ROOT, 'static/output')
    if not os.path.isdir(target_out):
        os.mkdir(target_out)
    
    # save the input image
    file = request.files.getlist("inputImage")[0]
    filename = file.filename
    input_path = "/".join([target_in, "in_" + user_adr + filename])
    output_path = "/".join([target_out, "out_" + user_adr + filename])
    # save the input image
    file.save(input_path)
    
    # get the paramters
    scale = int(request.form['scale'])
    #denoising_flag = request.form['denoising']
    smoothing_factor = request.form['smoothingFactor']
    

    # read the input image
    #img=cv2.imread(input_path)

    # run model Super resolution.
    compute_image(input_path, scale, output_path)

    # run models denoising if choice.
    if (request.form.get('denoising')) :
        test_ffdnet (output_path, output_path, cuda, int(smoothing_factor))

    time.sleep(1)
    return render_template("result.html", input = "in_" + user_adr + filename, output = "out_"+ user_adr + filename)





if __name__ == "__main__":
    app.run(debug=True)
