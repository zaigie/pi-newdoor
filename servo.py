#!/usr/bin/env python  
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
opened = 12
a = 10
b = 2
GPIO.setup(opened,GPIO.OUT)
pwm = GPIO.PWM(opened,50)

def OpenDoor(direction):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(open, GPIO.OUT)
    pwm.start(0)
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty)
    print("direction =", direction, "-> duty =", duty)
    time.sleep(1)

if __name__ == '__main__':
    GPIO.setup(opened, GPIO.OUT)
    OpenDoor(150)
    time.sleep(1)
    OpenDoor(0)
    GPIO.cleanup()
