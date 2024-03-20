import requests
import json
from RPLCD.i2c import CharLCD
# import RPLCD
# import smbus2

url = "http://127.0.0.1:5001"

# print("What would you like to test? \n1) Reset DB \n2) Add goal \n3) Add attempt")
# input = input()
# input = int(input)
# if input == 1:
#     request = requests.post(url+"/requests/reset", data = json.dumps({"message": "hello there"}), headers={"Content-Type": "Application/Json"})
#     print(request.text)
# elif input == 2:
#     request = requests.post(url+"/requests/goal")
#     print(request)

# elif input == 3:
#     request = requests.post(url+"/requests/attempt")
#     print(request)

attempts = requests.get(url+"/getAttempts") | 0
goals = requests.get(url+"/getGoals") | 0

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

lcd.write_string('Attempts: {attempts}\n\rGoals: {goals}')