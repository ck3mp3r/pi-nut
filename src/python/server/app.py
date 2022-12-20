#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/predict', methods=('POST'))
def predict_image():
    return app.make_response({
        "is_squirrel": False
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
