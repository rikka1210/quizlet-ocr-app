from flask import Flask, render_template, request, send_file
import os
import pytesseract
from PIL import Image
import csv
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    text = pytesseract.image_to_string(Image.open(image_path), lang='eng+jpn')
    lines = text.strip().split('\n')

    vocab_list = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            vocab_list.append([parts[0], ' '.join(parts[1:])])
        elif len(parts) == 1:
            vocab_list.append([parts[0], ''])

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_path = os.path.join(OUTPUT_FOLDER, f'quizlet_vocab_{timestamp}.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(vocab_list)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
