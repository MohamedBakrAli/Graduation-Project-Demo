
import os
from flask import Flask, request, redirect, url_for, render_template


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)



@app.route('/project')
def index ():
    return render_template("project.html")



@app.route('/demo', methods=['GET', 'POST'])
def demo ():
    if request.method == 'GET':
        
        return render_template("demo.html")
    elif request.method == 'POST':
        target = os.path.join(APP_ROOT, 'models/input')
        if not os.path.isdir(target):
            os.mkdir(target)
        
        print(target)
        print(request.files.getlist("inputImage"))
        print("===========")
        for file in request.files.getlist("inputImage"):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
            print("test")

        print("===========")
        return "complete"



if __name__ == "__main__":
  
    app.run(debug=True)