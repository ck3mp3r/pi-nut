FROM python:3.8-slim-bullseye

RUN python3 -m pip install tflite-runtime Flask
RUN mkdir -p /app/models
WORKDIR /app
COPY src/python /app

CMD /app/server/app.py
