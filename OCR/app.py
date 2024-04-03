import cv2
import easyocr
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

reader = easyocr.Reader(['en'])

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def process_image(file):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    img = cv2.imread(filepath)
    results = reader.readtext(img)
    recognized_text = [result[1] for result in results]
    return recognized_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        # Process the uploaded image for OCR
        recognized_text = process_image(file)
        return render_template('result.html', recognized_text=recognized_text)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)