# from time import sleep
import RPi.GPIO as GPIO
import time

PUL = 14  # Stepper Drive Pulses
DIR = 15  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 18  # Controller Enable Bit (High to Enable / LOW to Disable).

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

PIN_TRIGGER = 24
PIN_ECHO = 23

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.output(PIN_TRIGGER, GPIO.LOW)

print("Setting up Sensor")

print('Initialization Completed')
#
# Could have usesd only one DURATION constant but chose two. This gives play options.
durationFwd = 250 # This is the duration of the motor spinning. used for forward direction
durationBwd = 250 # This is the duration of the motor spinning. used for reverse direction

print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))

# delay = 0.0000001 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
delay = 0.00000001
print('Speed set to ' + str(delay))
#
cycles = 29 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
print('number of Cycles to Run set to ' + str(cycles))
angle = 0
#
#
def forward():
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    print('ENA set to HIGH - Controller Enabled')
    #
    time.sleep(.0005) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.LOW)
    # GPIO.output(DIRI, GPIO.LOW)
    print('DIR set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL being driven.')
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    print('ENA set to LOW - Controller Disabled')
    time.sleep(.0005) # pause for possible change direction
    return
#
#
def reverse():
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    print('ENA set to HIGH - Controller Enabled')
    #
    time.sleep(.005) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)
    # GPIO.output(DIRI, GPIO.HIGH)
    print('DIR set to HIGH - Moving Backward at ' + str(delay))
    print('Controller PUL being driven.')
    #
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    print('ENA set to LOW - Controller Disabled')
    time.sleep(.005) # pause for possible change direction
    return

isArmDown = False

while(isArmDown == False):
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time()

    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print("Distance:",distance,"cm")
    time.time.sleep(0.1)
    if(distance < 10):
        isArmDown = True
        break


if(isArmDown == True):
    while cyclecount < cycles:
        forward()
        cyclecount += 1
        angle += 1.8
        print("Angle: " + str(angle))
        print('Number of cycles completed: ' + str(cyclecount))
        print('Number of cycles remaining: ' + str(cycles - cyclecount))

    time.sleep(1)

    while cyclecount != 0:
        reverse()
        cyclecount -= 1
        angle += 1.8
        print("Angle: " + str(angle))
        print('Number of cycles completed: ' + str(cyclecount))
        print('Number of cycles remaining: ' + str(cycles - cyclecount))
#
GPIO.cleanup()
print('Cycling Completed')
#
