import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD

PUL = 14
DIR = 15
STEP = 0.9

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

pulses = 100
pulseDone = 0
delay = 0.00001
angle = 0

def moveMotor():
    GPIO.output(PUL, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(PUL, GPIO.LOW)
    time.sleep(delay)

while pulseDone <= pulses:
    GPIO.output(DIR, GPIO.HIGH)
    moveMotor()
    pulseDone += 1
    angle += STEP
    print("Angle: " + str(round(angle, 2)))

while pulseDone != 0:
    GPIO.output(DIR, GPIO.LOW)
    moveMotor()
    pulseDone += 1
    angle += STEP
    print("Angle: " + str(round(angle, 2)))