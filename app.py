from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import base64
from io import BytesIO

app = Flask(__name__)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

def preprocess_image(image):
    image = image.resize((224, 224))
    img_array = np.array(image)
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form['image']
    header, encoded = data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes))
    image.save("static/uploaded/captured.png")

    processed = preprocess_image(image)
    predictions = model.predict(processed)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]

    result = [(label, f"{prob*100:.2f}%") for (_, label, prob) in decoded]

    html = "<h2>Hasil Prediksi:</h2><ul>"
    for label, prob in result:
        html += f"<li>{label} — {prob}</li>"
    html += "</ul><img src='/static/uploaded/captured.png' width='300'>"
    return html

if __name__ == '__main__':
    os.makedirs('static/uploaded', exist_ok=True)
    app.run(debug=True)
