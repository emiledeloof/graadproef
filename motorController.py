# Bibliotheken importeren
import RPi.GPIO as GPIO
import time

#constante definiëren
PUL = 14  # Stepper Drive Pulses
DIR = 15  # Controller Direction Bit
PIN_TRIGGER = 24 # Ultrasoon Trig pin
PIN_ECHO = 23 # Ultrasoon Echo pin
step = 0.9 # hoek per stap

# BCM ipv Board
GPIO.setmode(GPIO.BCM)

# in- en outputs definiëren
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.output(PIN_TRIGGER, GPIO.LOW)

print("Setting up Sensor")
print('Initialization Completed')

durationFwd = 250 # This is the duration of the motor spinning. used for forward direction
durationBwd = 250 # This is the duration of the motor spinning. used for reverse direction

print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))

# tijd tussen pulsen, definieert motorsnelheid
delay = 0.00000001
print('Speed set to ' + str(delay))
#
cycles = 29 # aantal pulsen te versturen
cyclecount = 0 # aantal pulsen verstuurd
print('number of Cycles to Run set to ' + str(cycles))

def forward():
    time.sleep(.0005) # pauze tussen pulsen
    GPIO.output(DIR, GPIO.LOW) # geen pulsen sturen naar DIR pin op driver => CW draaien. 
    for x in range(durationFwd): 
        print("hello")
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay)
    time.sleep(.0005) # pause for possible change direction
    return
#
#
def reverse():
    print('ENA set to HIGH - Controller Enabled')
    time.sleep(.005) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)
    print('DIR set to HIGH - Moving Backward at ' + str(delay))
    print('Controller PUL being driven.')
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay)
    time.sleep(.005) # pause for possible change direction
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

GPIO.cleanup()
print('Cycling Completed')