from flask import Flask, request, send_file, render_template_string
import cv2
import numpy as np
import io
import os
import sys

# Add root to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.face_detection import detect_faces
from modules.face_blur import blur_faces
from modules.cartoonify import cartoonify
from modules.background_blur import blur_background
from modules.face_count import count_and_label_faces
from modules.filters import apply_grayscale, apply_sepia

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Face Processor API</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 40px auto; text-align: center; background: #1e1e2e; color: #cdd6f4; }
        .upload-section { border: 2px dashed #45475a; padding: 40px; border-radius: 10px; }
        select, input { margin: 10px; padding: 10px; border-radius: 5px; }
        button { background: #cba6f7; color: #11111b; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <h1>👤 Face Processor Web</h1>
    <div class="upload-section">
        <form action="/process" method="post" enctype="multipart/form-data">
            <input type="file" name="image" required><br>
            <select name="feature">
                <option value="detect">Face Detection</option>
                <option value="blur">Face Blur</option>
                <option value="count">Face Count</option>
                <option value="focus">Background Focus</option>
                <option value="cartoon">Cartoonify</option>
                <option value="gray">Grayscale</option>
                <option value="sepia">Sepia</option>
            </select><br>
            <button type="submit">Process Image</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return "No image uploaded", 400
    
    file = request.files['image']
    feature = request.form.get('feature', 'detect')
    
    # Read image
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(data, 1)
    
    # Process
    if feature == 'detect':
        output = detect_faces(image)
    elif feature == 'blur':
        output = blur_faces(image)
    elif feature == 'count':
        output = count_and_label_faces(image)
    elif feature == 'focus':
        output = blur_background(image)
    elif feature == 'cartoon':
        output = cartoonify(image)
    elif feature == 'gray':
        output = apply_grayscale(image)
    elif feature == 'sepia':
        output = apply_sepia(image)
    else:
        output = image

    # Encode result
    _, buffer = cv2.imencode('.jpg', output)
    io_buf = io.BytesIO(buffer)
    
    return send_file(io_buf, mimetype='image/jpeg')

# Vercel requires the app object to be named 'app'
# This file is used as a serverless function
