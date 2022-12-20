FROM python:3.8-slim-bullseye

RUN python3 -m pip install tflite-runtime
RUN mkdir -p /app
COPY src/python/requirements.txt /app
RUN python3 -m pip install -r /app/requirements.txt

WORKDIR /app
COPY src/python /app

CMD /app/server/app.py
