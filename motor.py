import RPi.GPIO as GPIO
import time
import requests
import json
import sys
from RPLCD.i2c import CharLCD

PUL = 14
DIR = 15
US1_TRIG = 24 # Ultrasoon1 Trig pin
US1_ECHO = 23 # Ultrasoon1 Echo pin
US2_TRIG = 27
US2_ECHO = 22
US3_TRIG = 25
US3_ECHO = 8
STEP = 0.9
URL = "https://swishbot.onrender.com/requests"

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

#US1
GPIO.setup(US1_TRIG, GPIO.OUT)
GPIO.setup(US1_ECHO, GPIO.IN)
GPIO.output(US1_TRIG, GPIO.LOW)

#US2
GPIO.setup(US2_TRIG, GPIO.OUT)
GPIO.setup(US2_ECHO, GPIO.IN)
GPIO.output(US2_TRIG, GPIO.LOW)

#US3
GPIO.setup(US3_TRIG, GPIO.OUT)
GPIO.setup(US3_ECHO, GPIO.IN)
GPIO.output(US3_TRIG, GPIO.LOW)

pulses = 60
pulseDone = 0
delay = 0.0005
delay2 = 0.001
angle = 0

isArmDown = False
isBallThrown = False

# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
# lcd.clear()
# print("LCD setup")

def refreshLCD():
    lcd.clear()
    attempts = requests.get(URL+"/getAttempts") 
    goals = requests.get(URL+"/getGoals")

    parsedAttempts = json.loads(attempts.text)
    parsedGoals = json.loads(goals.text)
    print(parsedGoals)
    percentage = float(parsedGoals['goals']) / float(parsedAttempts['attempts']) * 100
    percentage = int(percentage)

    lcd.write_string('Attempts: ' + str(parsedAttempts['attempts']) + "\n\rGoals: " + str(parsedGoals['goals']) + " => " + str(percentage) + "%")

def calculateDistance():
    pulse_end_time = 0
    pulse_start_time = 0
    GPIO.output(US1_TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(US1_TRIG, GPIO.LOW)

    while GPIO.input(US1_ECHO)==0:
        pulse_start_time = time.time()

    while GPIO.input(US1_ECHO)==1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print("Distance:",distance,"cm")
    time.sleep(0.01)
    return distance

def moveMotor():
    GPIO.output(PUL, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(PUL, GPIO.LOW)
    time.sleep(delay)


def moveMotorBack():
    GPIO.output(PUL, GPIO.HIGH)
    time.sleep(delay2)
    GPIO.output(PUL, GPIO.LOW)
    time.sleep(delay2)

# while True:
    # if(calculateDistance() < 10):
        # refreshLCD()
while pulseDone <= pulses:
            GPIO.output(DIR, GPIO.LOW)
            moveMotor()
            pulseDone += 1
            angle += STEP
            print("Angle: " + str(round(angle, 2)))

while pulseDone != 0:
    GPIO.output(DIR, GPIO.HIGH)
    moveMotorBack()
    pulseDone -= 1
    angle -= STEP
    print("Angle: " + str(round(angle, 2)))
