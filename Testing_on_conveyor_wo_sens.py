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
    send_command({"T":104, "x":78.28,"y":-1.92,"z":172.71,"t":3.10, "spd":0.15})
    
def go_to_pick():
    # send_command({"T":104, "x":490.2232692,"y":-168.6478844,"z":14.14464987,"t":2.40, "spd":0.15})
    # send_command({"T":104, "x":483.4499015,"y":-178.8597784,"z":22.03356826,"t":2.40, "spd":0.15})
    send_command({"T":102, "base":-0.35,"shoulder":1.28,"elbow":0.33,"hand":2.40, "spd":600, "acc":10})
                      
def close_gripper():
    send_command({"T":106, "cmd":3.10, "spd":0.15})
    
def open_gripper():
    send_command({"T":106, "cmd":2.40, "spd":0.15})
    
#--------PICK MOTION_WAYPOINTS--------
pick_waypoints = [
    {"base":-0.12,"shoulder":-0.036,"elbow":0.22,"hand":2.40},
    {"base":-0.33,"shoulder":1.35,"elbow":0.23,"hand":2.40},
]

def pick_motion():
    for i, point in enumerate(pick_waypoints):
        cmd = {"T":102, **point, "spd":600, "acc":10}
        print(f" Pick waypoint {i+1}/{len(pick_waypoints)}: {point}")
        send_command(cmd)
        time.sleep(0.7)

def pick_reverse():
    reversed_pick_waypoints = list(reversed(pick_waypoints))
    for i, point in enumerate(reversed_pick_waypoints):
        cmd = {"T":102, **point, "spd":600, "acc":10}
        print(f" Reverse pick waypoint {i+1}/{len(reversed_pick_waypoints)}: {point}")
        send_command(cmd)
        time.sleep(0.5)

#--------FLIP MOTION_WAYPOINTS--------
flip_waypoints = [
    {"base":-0.33,"shoulder":0.94,"elbow":0.18,"hand":3.10},
    {"base":-0.33,"shoulder":0.28,"elbow":0.18,"hand":3.10},
    {"base":-0.33,"shoulder":-0.13,"elbow":0.10,"hand":3.10},
    {"base":-2.73,"shoulder":-0.67,"elbow":0.10,"hand":3.10},
    {"base":-2.73,"shoulder":-1.48,"elbow":-0.08,"hand":3.10},
    {"base":-2.86,"shoulder":-1.70,"elbow":-0.01,"hand":3.10},
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
def handle_red():
    print("Object detected! Flip the object!")
    pick_motion()
    time.sleep(1)
    go_to_pick()
    time.sleep(0.5)
    close_gripper()
    time.sleep(0.5)
    flip_in_place()
    time.sleep(2.5)
    open_gripper()
    time.sleep(0.5)
    flip_in_reverse()
    time.sleep(2.5)       
    pick_reverse()
    time.sleep(1)
    # go_to_pick()
    # time.sleep(0.5)

    
def on_object_detected(colour):
    print(f"Detected colour: {colour}")
    if colour == "red":
        handle_red()
    # elif colour == "red":
    #     handle_red()
    else:
        print("Unknown colour, ignoring.")
    
while True:
    print("Robot Ghar ja raha hain....")
    go_home()
    fake_colour = input("Pretend the camera saw (red/black or quit): ").strip().lower()
    if fake_colour == "red":
        on_object_detected(fake_colour)
    else:
        print("Exiting....")
        break

# if __name__ == "__main__":
#     print("Starting up. Sending arm home first...")
#     go_home()
#     time.sleep(2)

#     print("Waiting for sensor to detect an object...")
#     while True:
#         sensor.wait_for_press()
#         handle_detection()
#         print("\n Waiting for next object...")
    