# Bibliotheken importeren
import RPi.GPIO as GPIO
import time
import requests
import json
from RPLCD.i2c import CharLCD

#constanten definieren
PUL = 14  # Driver PUL pin
DIR = 15  # Driver DIR pin
PIN_TRIGGER = 24 # Ultrasoon Trig pin
PIN_ECHO = 23 # Ultrasoon Echo pin
step = 0.9 # hoek per stap

url = "http://169.254.148.52:5001/requests"
url2 = "http://169.254.148.52:5001/"

GPIO.cleanup()

# BCM ipv Board
GPIO.setmode(GPIO.BCM)

# in- en outputs definieren
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.output(PIN_TRIGGER, GPIO.LOW)

print("Setting up Sensor")
print('Initialization Completed')

durationFwd = 250 # Aantal pulsen te sturen naar driver
durationBwd = 250 # Zelfde als hierboven maar voor omgekeerde richting

print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))

# tijd tussen pulsen, definieert motorsnelheid
delay = 0.00000001
print('Speed set to ' + str(delay))

cycles = 29 
cyclecount = 0 
print('number of Cycles to Run set to ' + str(cycles))

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()
print("LCD setup")

def refreshLCD():
    attempts = requests.get(url2+"/getAttempts") 
    goals = requests.get(url2+"/getGoals")

    print(attempts)

    parsedAttempts = json.loads(attempts.text)
    parsedGoals = json.loads(goals.text)

    percentage = parsedGoals['goals'] / parsedAttempts['attempts'] * 100
    print(percentage)

    lcd.write_string('Attempts: ' + str(parsedAttempts['attempts']) + "\n\rGoals: " + str(parsedGoals['goals']) + " => " + str(percentage) + "%")

while True:
    refreshLCD()
    def forward():
        time.sleep(.0005) # pauze tussen pulsen
        GPIO.output(DIR, GPIO.LOW) # geen pulsen sturen naar DIR pin op driver => CW draaien. 
        for x in range(durationFwd): # pulsen versturen naar driver
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(delay)
        time.sleep(.0005) 
        return

    def reverse():
        time.sleep(.005) 
        GPIO.output(DIR, GPIO.HIGH) # DIR CCW
        for y in range(durationBwd):
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(delay)
        return

    isArmDown = False

    while(isArmDown == False):
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()

        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:",distance,"cm")
        time.sleep(0.1)
        if(distance < 10):
            isArmDown = True
            break

    angle = 0 # effectieve hoek afh. van step
    if(isArmDown == True):
        time.sleep(0.5)
        while cyclecount < cycles:
            forward()
            cyclecount += 1
            angle += step
            print("Angle: " + str(round(angle, 2)))
            print('Number of cycles completed: ' + str(cyclecount))
            print('Number of cycles remaining: ' + str(cycles - cyclecount))

        time.sleep(2)

        while cyclecount != 0:
            reverse()
            cyclecount -= 1
            angle -= step
            print("Angle: " + str(round(angle, 2)))
            print('Number of cycles completed: ' + str(cyclecount))
            print('Number of cycles remaining: ' + str(cycles - cyclecount))
        
        isArmDown = False
        request = requests.post(url+"/attempt")
    if(angle > 360):
        break

GPIO.cleanup()
print('Cycling Completed')