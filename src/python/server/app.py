#!/usr/bin/env python3

from flask import Flask, request
from tflite_runtime.interpreter import Interpreter
from PIL import Image
import time
import numpy as np


UPLOAD_FOLDER = '/app/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

data_folder = "/app/models/"

model_path = data_folder + "mobilenet_v1_1.0_224_quant.tflite"
label_path = data_folder + "labels_mobilenet_quant_v1_224.txt"

interpreter = Interpreter(model_path)
print("Model Loaded Successfully.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print("Image Shape (", width, ",", height, ")")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/predict', methods=['POST'])
def predict_image():

    file = request.files.get('file', None)

    if file is not None and allowed_file(file.filename):
        image = Image.open(file.stream).convert(
            'RGB').resize((width, height))
        # Classify the image.
        time1 = time.time()
        label_id, prob = classify_image(interpreter, image)
        time2 = time.time()
        classification_time = np.round(time2-time1, 3)
        print("Classificaiton Time =", classification_time, "seconds.")
        # Read class labels.
        labels = load_labels(label_path)

        # Return the classification label of the image.
        classification_label = labels[label_id]
        print("Image Label is :", classification_label,
              ", with Accuracy :", np.round(prob*100, 2), "%.")

    return app.make_response({
        "confidence": np.round(prob*100, 2),
        "object": classification_label
    })


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def classify_image(interpreter, image, top_k=1):
    set_input_tensor(interpreter, image)

    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]][0]


def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image


def load_labels(path):  # Read the labels from the text file as a Python list.
    with open(path, 'r') as f:
        return [line.strip() for i, line in enumerate(f.readlines())]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
