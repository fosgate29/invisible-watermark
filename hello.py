import cv2
import hashlib
from imwatermark import WatermarkEncoder
from imwatermark import WatermarkDecoder
from PIL import Image
import os
from flask import Flask, flash, request, redirect, url_for, json, jsonify
from werkzeug.utils import secure_filename

from flask import send_from_directory

from random import seed
from random import randint
import imagehash

UPLOAD_FOLDER = '/home/ubuntu/nft'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/random/")
def randomnumber():
    #seed(1)
    value = randint(0, 9999999999999999999999999999)
    print(value)
    return str(value)

@app.route("/test/")
def hello_world():
    bgr = cv2.imread('original.jpg')
    wm = 'test'

    encoder = WatermarkEncoder()
    encoder.set_watermark('bytes', wm.encode('utf-8'))
    bgr_encoded = encoder.encode(bgr, 'dwtDct')

    cv2.imwrite('test_wm.png', bgr_encoded)

    bgr = cv2.imread('test_wm.png')

    decoder = WatermarkDecoder('bytes', 32)
    watermark = decoder.decode(bgr, 'dwtDct')
    #print(watermark.decode('utf-8'))

    return watermark.decode('utf-8')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            bgr = cv2.imread(filename)
            value = randint(0, 9999)
            wm = str(value)
            print(wm)
            encoder = WatermarkEncoder()
            encoder.set_watermark('bytes', wm.encode('utf-8'))
            bgr_encoded = encoder.encode(bgr, 'dwtDct')
            cv2.imwrite('test_wm.png', bgr_encoded)
            
            bgr = cv2.imread('test_wm.png')
            length = encoder.get_length()
            decoder = WatermarkDecoder('bytes', length)
            watermark = decoder.decode(bgr, 'dwtDct')
            print(watermark.decode('utf-8'))    
       
            hash1 = ''
            hash2 = ''
            name2 = "test_wm.png"
            with open(name2,"rb") as f:
               bytes = f.read() # read entire file as bytes
               hash1 = hashlib.sha256(bytes).hexdigest();
               print(hash1)

            name2 = filename
            with open(name2,"rb") as f:
               bytes = f.read() # read entire file as bytes
               hash2 = hashlib.sha256(bytes).hexdigest();
               print(hash2)

            name2 = filename
            with open(name2,"rb") as f:
               bytes = f.read() # read entire file as bytes
               hash2 = hashlib.sha256(bytes).hexdigest();
               print(hash2)

            result = jsonify(
              originalfilehash = str(hash2),
              wmfilehash = str(hash1),
              randomnumber= wm,
              wmfileurl=url_for('download_file', name='test_wm.png')
            )

            return result
            #return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
