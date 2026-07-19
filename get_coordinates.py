import requests
import json
import time

arm_ip = "192.168.4.1"

def send_command(cmd_dict):
    command = json.dumps(cmd_dict)
    url = f"http://{arm_ip}/js?json={command}"
    response = requests.get(url)
    return response.text


result = send_command({"T":210, "cmd":0})
print("Arm unlocked, you can now move it by hand:", result)


get_coord = send_command({"T":105})
print(get_coord)