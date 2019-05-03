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
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<on>/<yes>")
def mainopen():
    os.system("python3 servo.py ")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080, debug=True, threaded=True)