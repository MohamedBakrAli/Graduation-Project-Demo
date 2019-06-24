import os, time, sys
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


def remove(path):
    """
    Remove the file or directory
    """
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except OSError:
            print ("Unable to remove folder: %s" % path)
    else:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            print ("Unable to remove file: %s" % path)
 
def cleanup(number_of_days, path):
    """
    Removes files from the passed in path that are older than or equal 
    to the number_of_days
    """
    time_in_secs = time.time() - (number_of_days * 24 * 60 * 60)
    for root, dirs, files in os.walk(path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)
 
            if stat.st_mtime <= time_in_secs:
                remove(full_path)
 
       
 

@cron.interval_schedule(hours = 4)
def delete_temporary_files():
    input_path = os.path.join(APP_ROOT, 'static/input')
    output_path = os.path.join(APP_ROOT, 'static/output')
    cleanup(1, input_path)
    cleanup(1, output_path)



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
    
    # run model Super resolution.
    if (request.form.get('superResolution')):
        scale = int(request.form['scale'])
        compute_image(input_path, scale, output_path)

    # run models denoising if choice.
    if (request.form.get('denoising') and request.form.get('superResolution')):
        smoothing_factor = request.form['smoothingFactor']

        if (smoothing_factor == 'Auto'):
            smoothing_factor = estimate_noise(output_path)
        else:
            smoothing_factor = int(smoothing_factor)

        test_ffdnet (output_path, output_path, cuda, smoothing_factor)
        
    elif (request.form.get('denoising')):
        smoothing_factor = request.form['smoothingFactor']

        if (smoothing_factor == 'Auto'):
            smoothing_factor = estimate_noise(input_path)
        else:
            smoothing_factor = int(smoothing_factor)

        test_ffdnet (input_path, output_path, cuda, smoothing_factor)
            

    return render_template("result.html", input = "in_" + user_adr + filename, output = "out_"+ user_adr + filename)




if __name__ == "__main__":
    app.run(debug=True)
