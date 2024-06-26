import RPi.GPIO as GPIO
import time
import requests
import json
import sys
from RPLCD.i2c import CharLCD
import random

PUL = 14
DIR = 15
US1_TRIG = 24 # Ultrasoon1 Trig pin // Arm beneden?
US1_ECHO = 23 # Ultrasoon1 Echo pin
US2_TRIG = 25   # bal in arm?
US2_ECHO = 8
US3_TRIG = 27   #gescoord?
US3_ECHO = 17
STEP = 1.8
# URL = "https://swishbot.onrender.com/requests"
URL = "http://192.168.0.101:5001/requests"

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

pulses = 22
pulseDone = 0
delay = 0.0011
delay2 = 0.008
angle = 0

isArmDown = False
isBallThrown = False

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()
print("LCD setup")
lcd.write_string("swishbot.onrender.com")

def refreshLCD():
    lcd.clear()
    attempts = requests.get(URL+"/getAttempts") 
    goals = requests.get(URL+"/getGoals")
    print(attempts)

    parsedAttempts = json.loads(attempts.text)
    parsedGoals = json.loads(goals.text)
    
    percentage = float(parsedGoals['goals']) / float(parsedAttempts['attempts']) * 100
    percentage = int(percentage)

    lcd.write_string('Schoten: ' + str(parsedAttempts['attempts']) + "\n\rGoals: " + str(parsedGoals['goals']) + " => " + str(percentage) + "%")
    # lcd.write_string(str(random.randint(0,10)))

def calculateDistanceArm():
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
    # print("Distance:",distance,"cm")
    time.sleep(0.01)
    return distance

def calculateDistanceBall():
    pulse_end_time = 0
    pulse_start_time = 0
    GPIO.output(US2_TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(US2_TRIG, GPIO.LOW)

    while GPIO.input(US2_ECHO)==0:
        pulse_start_time = time.time()

    while GPIO.input(US2_ECHO)==1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    # print("Distance:",distance,"cm")
    time.sleep(0.1)
    return distance

def calculateDistanceGoal():
    pulse_end_time = 0
    pulse_start_time = 0
    GPIO.output(US3_TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(US3_TRIG, GPIO.LOW)

    while GPIO.input(US3_ECHO)==0:
        pulse_start_time = time.time()

    while GPIO.input(US3_ECHO)==1:
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

while True:
    if(calculateDistanceArm() < 10):
        if(calculateDistanceBall() < 5):
            refreshLCD()
            requests.post(URL+"/attempt")
            time.sleep(1)
            i = 0
            goal = False
            while pulseDone <= pulses:
                GPIO.output(DIR, GPIO.LOW)
                moveMotor()
                pulseDone += 1
                angle += STEP
                # print("Angle: " + str(round(angle, 2)))
            time.sleep(1.5)
            for i in range(10):
                if(calculateDistanceGoal() < 12 or calculateDistanceGoal() > 1200):
                    lcd.clear()
                    lcd.write_string("GOAL!")
                    goal = True
                    i = 9
            if(goal == True):
                requests.post(URL+"/goal")
    else:
        time.sleep(0.5)
        while calculateDistanceArm() > 10:
            GPIO.output(DIR, GPIO.HIGH)
            moveMotorBack()
            angle -= STEP
            # print("Angle: " + str(round(angle, 2)))
        pulseDone = 0
        time.sleep(1)
