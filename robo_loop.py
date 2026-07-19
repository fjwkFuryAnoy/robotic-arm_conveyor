import requests
import json
import time
from gpiozero import Button

#-------- SETUP --------
arm_ip = "192.168.4.1"
sensor = Button(17)

def send_command(cmd_dict):
    command = json.dumps(cmd_dict)
    url = f"http://{arm_ip}/js?json={command}"
    return requests.get(url).text


#-------- DEFINING BASIC MOVES --------
def go_home():
    send_command({"T":104, "x":158.4644718,"y":184.2751415,"z":172.1359459,"t":0, "spd":0.15})
    
def go_to_pick():
    send_command({"T":104, "x":404.9635459,"y":320.0541147,"z":-49.90927037,"t":0, "spd":0.15})
                      
def close_gripper():
    send_command({"T":106, "cmd":3.10, "spd":0.15})
    
def open_gripper():
    send_command({"T":106, "cmd":2.32, "spd":0.15})
    

#--------FLIP MOTION_WAYPOINTS--------
flip_waypoints = [
    {"base":0.88,"shoulder":1.5,"elbow":0.09,"hand":3.1},
    {"base":0.88,"shoulder":0.5,"elbow":0.1,"hand":3.1},
    {"base":0.92,"shoulder":-0.01,"elbow":0.1,"hand":3.1},
    {"base":-1.4,"shoulder":-0.13,"elbow":0.08,"hand":3.1},
    {"base":-1.4,"shoulder":-1.0,"elbow":0.08,"hand":3.1},
    {"base":-1.4,"shoulder":-1.7,"elbow":-0.1,"hand":3.1},
]

def flip_in_place():
    for i, point in enumerate(flip_waypoints):
        cmd = {"T":102, **point, "spd":600, "acc":10}
        print(f" Flip waypoint {i+1}/{len(flip_waypoints)}: {point}")
        send_command(cmd)
        time.sleep(0.7)
        
def flip_in_reverse():
    reversed_waypoints = list(reversed(flip_waypoints))
    for i, point in enumerate(reversed_waypoints):
        cmd = {"T":102, **point, "spd":600, "acc":10}
        print(f" Reverse waypoint {i+1}/{len(reversed_waypoints)}: {point}")
        send_command(cmd)
        time.sleep(0.5)
        

#--------FULL SEQUENCES--------  
def handle_detection():
    print("Object detected! Flip the object!")
    go_to_pick()
    time.sleep(0.5)
    close_gripper()
    time.sleep(0.5)
    flip_in_place()
    time.sleep(2)
    open_gripper()
    time.sleep(0.5)
    flip_in_reverse()
    time.sleep(2)
    go_to_pick()
    time.sleep(0.5)

    
# def on_object_detected(colour):
#     print(f"Detected colour: {colour}")
#     if colour == "black":
#         handle_black()
#     elif colour == "red":
#         handle_red()
#     else:
#         print("Unknown colour, ignoring.")
    
# while True:
#     fake_colour = input("Pretend the camera saw (red/black or quit): ").strip().lower()
#     if fake_colour == "quit":
#         print("Exiting....")
#         break
#     on_object_detected(fake_colour)

if __name__ == "__main__":
    print("Starting up. Sending arm home first...")
    go_home()
    time.sleep(2)

    print("Waiting for sensor to detect an object...")
    while True:
        sensor.wait_for_press()
        handle_detection()
        print("\n Waiting for next object...")
    
    
    