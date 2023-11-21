from fastapi import FastAPI

import cv2
import threading
import time
from djitellopy import Tello

global tello
tello = None

global continue_receive_video
continue_receive_video = False


def ReceiveVideo():
    global tello
    global continue_receive_video
    while True:
        if not continue_receive_video:
            break
        frame_read = tello.get_frame_read()
        frame = frame_read.frame
        cv2.imshow("Tello", frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()

video_thread = threading.Thread(target=ReceiveVideo)


app = FastAPI(
    title="Tello API",
    description="API for controlling the Tello drone",
    version="0.0.1",
)

@app.get("/tello/init")
async def init_tello():
    global tello
    if tello is None:
        tello = Tello()
        tello.connect()
        return "Ok"
    else:
        return "Already initialized"


@app.get("/tello/kill")
async def kill_tello():
    global tello
    global continue_command_tello
    if tello is None:
        return "Not initialized"
    tello.end()
    tello = None
    return "Ok"

@app.get("/tello/streamon")
async def streamon_tello():
    """
    Start the video stream
    """
    global tello
    global continue_receive_video

    tello.streamon()
    continue_receive_video = True
    video_thread.start()
    return "Ok"

@app.get("/tello/streamoff")
async def streamoff_tello():
    """
    Stop the video stream
    """
    global tello
    global continue_receive_video

    continue_receive_video = False
    video_thread.join()
    tello.streamoff()
    return "Ok"

    
@app.get("/tello/takeoff")
async def takeoff_tello():
    """
    Command the drone to takeoff
    """
    global tello
    tello.takeoff()
    return "Ok"

@app.get("/tello/land")
async def land_tello():
    """
    Command the drone to land
    """
    global tello
    tello.land()
    return "Ok"

@app.get("/tello/emergency")
async def emergency_tello():
    """
    Command the drone to stop all motors
    """
    global tello
    tello.emergency()
    return "Ok"

@app.get("/tello/up")
async def up_tello(distance: int):
    """
    Command the drone to move up 'distance' cm
    """
    global tello
    tello.move_up(distance)
    return "Ok"

@app.get("/tello/down")
async def down_tello(distance: int):
    """
    Command the drone to move down 'distance' cm
    """
    global tello
    tello.move_down(distance)
    return "Ok"

@app.get("/tello/left")
async def left_tello(distance: int):
    """
    Command the drone to move left 'distance' cm
    """
    global tello
    tello.move_left(distance)
    return "Ok"

@app.get("/tello/right")
async def right_tello(distance: int):
    """
    Command the drone to move right 'distance' cm
    """
    global tello
    tello.move_right(distance)
    return "Ok"

@app.get("/tello/forward")
async def forward_tello(distance: int):
    """
    Command the drone to move forward 'distance' cm
    """
    global tello
    tello.move_forward(distance)
    return "Ok"

@app.get("/tello/back")
async def back_tello(distance: int):
    """
    Command the drone to move back 'distance' cm
    """
    global tello
    tello.move_back(distance)
    return "Ok"

@app.get("/tello/cw")
async def cw_tello(angle: int):
    """
    Command the drone to rotate clockwise 'angle' degrees
    """
    global tello
    tello.rotate_clockwise(angle)
    return "Ok"

@app.get("/tello/ccw")
async def ccw_tello(angle: int):
    """
    Command the drone to rotate counter-clockwise 'angle' degrees
    """
    global tello
    tello.rotate_counter_clockwise(angle)
    return "Ok"

@app.get("/tello/flip")
async def flip_tello(direction: str):
    """
    Command the drone to flip in the direction 'direction'
    """
    global tello
    tello.flip(direction)
    return "Ok"

@app.get("/tello/go")
async def go_tello(x: int, y: int, z: int, speed: int):
    """
    Command the drone to go to the position (x, y, z) at speed 'speed'
    """
    global tello
    tello.go(x, y, z, speed)
    return "Ok"

@app.get("/tello/curve")
async def curve_tello(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: int):
    """
    Command the drone to go to the position (x2, y2, z2) at speed 'speed' while passing through (x1, y1, z1)
    """
    global tello
    tello.curve(x1, y1, z1, x2, y2, z2, speed)
    return "Ok"

@app.get("/tello/set-speed")
async def set_speed_tello(speed: int):
    """
    Command the drone to set the speed to 'speed'
    """
    global tello
    tello.set_speed(speed)
    return "Ok"

@app.get("/tello/rc")
async def rc_tello(left_right_velocity: int, forward_backward_velocity: int, up_down_velocity: int, yaw_velocity: int):
    """
    Command the drone to set the speed to 'speed'
    """
    global tello
    tello.send_rc_control(left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity)
    return "Ok"

@app.get("/tello/get-battery")
async def get_battery_tello():
    """
    Get the battery percentage of the drone
    """
    global tello
    return tello.get_battery()

@app.get("/tello/get-speed")
async def get_speed_tello():
    """
    Get the speed of the drone
    """
    global tello
    return tello.get_speed()

@app.get("/tello/get-time")
async def get_time_tello():
    """
    Get the flight time of the drone
    """
    global tello
    return tello.get_flight_time()

@app.get("/tello/get-wifi")
async def get_wifi_tello():
    """
    Get the wifi signal strength of the drone
    """
    global tello
    return tello.get_wifi()
