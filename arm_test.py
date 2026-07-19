import requests
import json
import time

arm_ip = "192.168.4.1"

def send_command(cmd_dict):
    command = json.dumps(cmd_dict)
    url = f"http://{arm_ip}/js?json={command}"
    response = requests.get(url)
    return response.text

print("Step 1: Asking arm for its CURRENT position...")
before = send_command({"T": 105})
print("Current position:", before)

time.sleep(2)

print("\nStep 2: Telling the arm to MOVE to a new position...")
send_command({"T": 1041, "x": 100, "y": 100, "z": 200, "t":0})
print("Move command sent! Watch the arm now.")

time.sleep(3)

print("\nStep 3: Asking arm for position AGAIN...")
after = send_command({"T": 105})
print("New position:", after)

print("\n Done! If the numbers in 'before' and 'after' are different AND you saw it move, it worked!")