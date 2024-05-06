# import RPi.GPIO as GPIO
import time
import random

allDistances = []
averageDistance = 0

def average(distance, averageDistance, allDistances):
    if(averageDistance != 0):
        averageDistance = (averageDistance + distance) / 2
    if(len(allDistances) == 2):
        averageDistance = (allDistances[0] + allDistances[1]) / 2
    return averageDistance


while (True):  
    time.sleep(0.5)
    distance = random.randint(1,10)
    allDistances.append(distance)
    print(average(distance, averageDistance, allDistances))
    print(allDistances)
    time.sleep(0.5)

# try:
#     GPIO.setmode(GPIO.BCM)
#     PIN_TRIGGER = 24
#     PIN_ECHO = 23

#     GPIO.setup(PIN_TRIGGER, GPIO.OUT)
#     GPIO.setup(PIN_ECHO, GPIO.IN)
#     GPIO.output(PIN_TRIGGER, GPIO.LOW)

#     print("Setting up Sensor")

#     while(True):
#         GPIO.output(PIN_TRIGGER, GPIO.HIGH)
#         time.sleep(0.00001)
#         GPIO.output(PIN_TRIGGER, GPIO.LOW)

#         pulse_start_time = 0
#         pulse_end_time = 0

#         while GPIO.input(PIN_ECHO)==0:
#             pulse_start_time = time.time()

#         while GPIO.input(PIN_ECHO)==1:
#             pulse_end_time = time.time()

#         pulse_duration = pulse_end_time - pulse_start_time
#         distance = round(pulse_duration * 17150, 2)
#         allDistances.append(distance)
#         average(allDistances)
        # if():
        #     break;

# finally:
#     GPIO.cleanup()