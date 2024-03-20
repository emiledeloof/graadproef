import requests
import json
from RPLCD.i2c import CharLCD
# import RPLCD
# import smbus2

url = "http://192.168.0.101:5001/requests"

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

attempts = requests.get(url+"/getAttempts") 
goals = requests.get(url+"/getGoals")

parsedAttempts = json.loads(attempts.text)
parsedGoals = json.loads(goals.text)

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

lcd.write_string('Attempts: ' + str(parsedAttempts['attempts']) + "\n\rGoals: " + str(parsedGoals['goals']) + "    => " + str(parsedAttempts['attempts'] / parsedGoals['goals']))
