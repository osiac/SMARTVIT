import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import untitled1
import glob
# import numpy as np
# from keras.models import load_model
# import paho.mqtt.publish as publicare
# import glob
# from PIL import Image, ImageOps
# import json

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # else:
    #	flash('Allowed image types are -> png, jpg, jpeg, gif')
    #	return redirect(request.url)

    return render_template('index.html', filenames=file_names)

@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/analyse')
def display():
    # print('display_image filename: ' + filename)
    untitled1.message()
    for pic in glob.glob("static/uploads/*"):
        os.remove(pic)
    return render_template('analyse.html') 

if __name__ == "__main__":
    app.run(host='0.0.0.0')