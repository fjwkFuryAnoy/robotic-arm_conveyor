import requests

arm_ip = "192.168.4.1"
command = '{"T":105}'

url = f"http://{arm_ip}/js?json={command}"
response = requests.get(url)
print(response.text)