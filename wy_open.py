# encoding: utf-8
import os
import time
from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(BOARD)
GPIO.setwarnings(False)
open = 12
fPWM = 50
a = 10
b = 2
GPIO.setup(open, GPIO.OUT)
pwm = GPIO.PWM(open, fPWM)

def OpenDoor(direction):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(open, GPIO.OUT)
    pwm.start(0)
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty)
    print("direction =", direction, "-> duty =", duty)
    time.sleep(1)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/open")
def mainopen():
    OpenDoor(45)
    time.sleep(0.5)
    OpenDoor(0)
    GPIO.cleanup()
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080, debug=True, threaded=True)