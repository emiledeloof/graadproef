import requests
import json
# import RPLCD
# import smbus2

url = "http://127.0.0.1:5001"

print("What would you like to test? \n1) Reset DB \n2) Add goal \n3) Add attempt")
input = input()
input = int(input)
if input == 1:
    request = requests.post(url+"/requests/reset", data = json.dumps({"message": "hello there"}), headers={"Content-Type": "Application/Json"})
    print(request.text)
elif input == 2:
    request = requests.post(url+"/requests/goal")
    print(request)

elif input == 3:
    request = requests.post(url+"/requests/attempt")
    print(request)

