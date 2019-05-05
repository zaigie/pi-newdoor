#!/usr/bin/env python  
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
open = 12
a = 10
b = 2
GPIO.setup(open,GPIO.OUT)
pwm = GPIO.PWM(open,50)

def OpenDoor(direction):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(open, GPIO.OUT)
    pwm.start(0)
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty)
    print("direction =", direction, "-> duty =", duty)
    time.sleep(1)

if __name__ == '__main__':
    GPIO.setup(open, GPIO.OUT)
    OpenDoor(162)
    pwm.stop()
    GPIO.cleanup()
