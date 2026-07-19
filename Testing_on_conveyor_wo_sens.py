import requests
import json
import time
from gpiozero import Button

#-------- SETUP --------
m = 0
arm_ip = "192.168.4.1"
sensor_pin = 17

sensor=Button(sensor_pin, pull_up=False, bounce_time=0.2)

# SAFE_LIMITS = {
#     "base":(-3.14,3.14),
#     "shoulder":(-1.57,1.57),
#     "elbow":(0,3.14),
#     "hand":(0,3.14),
# }

busy=False

# def is_safe(cmd_dict):
#     for key, value in cmd_dict.items():
#         if key in SAFE_LIMITS:
#             low, high = SAFE_LIMITS[key]
#             if not(low<=value<=high):
#                 print(f"UNSAFE VALUE: {key}={value} outside allowed range {SAFE_LIMITS[key]}")
#                 return False
#     return True

def send_command(cmd_dict, timeout=3):
    # if not is_safe(cmd_dict):
    #     return None
    command = json.dumps(cmd_dict)
    url = f"http://{arm_ip}/js?json={command}"
    try:
        response = requests.get(url, timeout=timeout)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"COMMUNICATION ERROR: {e}")
        return None


#-------- DEFINING BASIC MOVES --------
def go_home():
    send_command({"T":104, "x":78.28,"y":-1.92,"z":172.71,"t":3.10, "spd":0.15})
    
def go_to_pick():
    # send_command({"T":104, "x":490.2232692,"y":-168.6478844,"z":14.14464987,"t":2.40, "spd":0.15})
    # send_command({"T":104, "x":483.4499015,"y":-178.8597784,"z":22.03356826,"t":2.40, "spd":0.15})
    send_command({"T":102, "base":-0.35,"shoulder":1.23,"elbow":0.46,"hand":2.40, "spd":600, "acc":10})
    m = 1
                      
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
    m = 1
    for i, point in enumerate(pick_waypoints):
        cmd = {"T":102, **point, "spd":600, "acc":10}
        print(f" Pick waypoint {i+1}/{len(pick_waypoints)}: {point}")
        send_command(cmd)
        time.sleep(0.7)


def pick_reverse():
    m = 1
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
    {"base":-2.86,"shoulder":-1.57,"elbow":-0.31,"hand":3.10},
]

def flip_in_place():
    for i, point in enumerate(flip_waypoints):
        if i<=3:
            m = 1
        else:
            m = 2
        cmd = {"T":102, **point, "spd":600, "acc":10}
        print(f" Flip waypoint {i+1}/{len(flip_waypoints)}: {point}")
        send_command(cmd)
        time.sleep(0.7)
        
def flip_in_reverse():
    reversed_waypoints = list(reversed(flip_waypoints))
    for i, point in enumerate(reversed_waypoints):
        if i<=3:
            m = 2
        else:
            m = 1
        cmd = {"T":102, **point, "spd":600, "acc":10}
        print(f" Reverse waypoint {i+1}/{len(reversed_waypoints)}: {point}")
        send_command(cmd)
        time.sleep(0.5)
        
        

#--------FULL SEQUENCES--------  
# def handle_red():
#     print("Object detected! Flip the object!")
#     pick_motion()
#     time.sleep(1)
#     go_to_pick()
#     time.sleep(0.5)
#     close_gripper()
#     time.sleep(0.5)
#     flip_in_place()
#     time.sleep(2.5)
#     open_gripper()
#     time.sleep(0.5)
#     flip_in_reverse()
#     time.sleep(2.5)       
#     # pick_reverse()
#     # time.sleep(1)
#     go_to_pick()
#     time.sleep(0.5)

def handle_detection():
    print("Object detected! Flip the object!")
    # pick_motion()
    # time.sleep(1)
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
    # pick_reverse()
    # time.sleep(1)
    go_to_pick()
    time.sleep(0.5)


def emergency_stop():
    print("Emergency Stop triggered, Robot ja raha ghar!!!")
    open_gripper()
    time.sleep(0.5)
    if m==2:
        flip_in_reverse()
        time.sleep(5)
        go_home()
        time.sleep(2)
    else:
        go_home()
        time.sleep(2)

    
# def on_object_detected(colour):
#     print(f"Detected colour: {colour}")
#     if colour == "red":
#         handle_red()
#     # elif colour == "red":
#     #     handle_red()
#     else:
#         print("Unknown colour, ignoring.")
    
# while True:
#     print("Return to base....")
#     go_home()
#     fake_colour = input("Pretend the camera saw (red/black or quit): ").strip().lower()
#     if fake_colour == "red":
#         on_object_detected(fake_colour)
#     else:
#         print("Exiting....")
#         break

if __name__ == "__main__":
    try:
        print("Starting up. Sending arm home first (one-time only)...")
        go_home()
        time.sleep(2)
        pick_motion()
        time.sleep(1)
        print("Moving to pick point and waiting there...")
        go_to_pick()

        print("Waiting for sensor to detect an object...")
        while True:
            sensor.wait_for_press()
            time.sleep(0.25)
            handle_detection()
            print("\nBack at pick point. Waiting for next object...")
            
    except KeyboardInterrupt:
        emergency_stop()
        print("Shutdown Complete")
