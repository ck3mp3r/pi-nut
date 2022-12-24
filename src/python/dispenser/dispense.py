#!/usr/bin/env python3

import argparse
import logging
import requests
import RPi.GPIO as GPIO
import time


# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/detective.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--image", help="Full path to image file.")
parser.add_argument("-s", "--service", help="Prediction service end point.",
                    default="http://tflite.mb.lab/predict")
args = parser.parse_args()


def run_programm():
    if args.image:
        detect_squirrel(args.image)


def detect_squirrel(image):
    logger.debug(image)
    image_file = open(image, "rb")
    response = requests.post(args.service, files={"file": image_file})

    confidence, object = (
        response.json()["confidence"], response.json()["object"])

    logger.debug(confidence)
    logger.debug(object)
    if (confidence > 40
            and any(word in object for word
                    in ["porcupine", "squirrel", "mongoose", "hamster"])):
        dispense()


def dispense():
    logger.debug("Dispensing!")
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(0)  # Initialization
    p.ChangeDutyCycle(8)
    time.sleep(3.80)
    GPIO.cleanup()
    logger.debug("Done!")


if __name__ == "__main__":
    run_programm()
