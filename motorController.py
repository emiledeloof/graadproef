from time import sleep
import RPi.GPIO as GPIO

PUL = 14  # Stepper Drive Pulses
DIR = 15  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 18  # Controller Enable Bit (High to Enable / LOW to Disable).

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

print('Initialization Completed')

durationFwd = 5000 # This is the duration of the motor spinning. used for forward direction
durationBwd = 5000 # This is the duration of the motor spinning. used for reverse direction
print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))

# delay = 0.0000001 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
delay = 0.0000000001
print('Speed set to ' + str(delay))
#
cycles = 10 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
print('number of Cycles to Run set to ' + str(cycles))
#
#
def forward():
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    print('ENA set to HIGH - Controller Enabled')
    #
    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.LOW)
    # GPIO.output(DIRI, GPIO.LOW)
    print('DIR set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL being driven.')
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    print('ENA set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return
#
#
def reverse():
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    print('ENA set to HIGH - Controller Enabled')
    #
    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)
    # GPIO.output(DIRI, GPIO.HIGH)
    print('DIR set to HIGH - Moving Backward at ' + str(delay))
    print('Controller PUL being driven.')
    #
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    print('ENA set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return

while cyclecount < cycles:
    forward()
    # reverse()
    cyclecount = (cyclecount + 1)
    print('Number of cycles completed: ' + str(cyclecount))
    print('Number of cycles remaining: ' + str(cycles - cyclecount))
#
GPIO.cleanup()
print('Cycling Completed')
#