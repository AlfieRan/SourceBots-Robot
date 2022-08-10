from sbot import Robot
from sbot.env import ConsoleEnvironment, HardwareEnvironment
import localisation
import movement
import time


ROBOT = Robot(wait_start=False, debug=True) # create the robot object
ARDUINO = ROBOT.arduino     # get the arduino object
TOKEN_ID = ROBOT.zone + 28
MOVEMENT = movement.get_movement(ROBOT, TOKEN_ID) # get the movement object
LOCAL = localisation.local(ROBOT)

def setup():
    print("Running Setup...")
    # this is when the file would be read to see what bot we are - what colour we're aiming for
    return

def init():
    print("Launching...")
    setup() # stuff to be ran before bot launches
    ROBOT.wait_start() # start the robot
    return

def main():
    Running = True
    ### game plan
    # position right, go forward until collected 3 tokens
    img_markers = ROBOT.camera.see()

    # go left, dump them in the first zone
    # turn left and go forward a bit

    # loop:
    while Running:
        # go to nearest token
        MOVEMENT.goto_nearest_token()
        # check if the token is already in the scoring zone
        in_scoring = False # replace this with some kind of function
        # [function] collect token using sweep method
        MOVEMENT.sweep_collect()
        MOVEMENT.collision_avoidance()
        MOVEMENT.set_forward()
        time.sleep(100)
        MOVEMENT.stop()
        # move back to scoring zone
        MOVEMENT.goto_pos(0,0) # replace this with a scoring zone - maybe try and get 3 tokens in a zone or something??

    pass

init()
print("Finished Running")