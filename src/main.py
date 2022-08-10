from sbot import Robot
from sbot.env import ConsoleEnvironment, HardwareEnvironment
import movement

# code based constants - don't change these unless you know what you're doing
ROBOT = Robot(wait_start=False, debug=True) # create the robot object
# ARDUINO = ROBOT.arduino     # get the arduino object
MOVEMENT = movement.get_movement(ROBOT) # get the movement object

def setup():
    print("Running Setup...")
    # this is when the file would be read to see what bot we are - what colour we're aiming for
    return

def init():
    print("Launching...")
    setup() # stuff to be ran before bot launches
    ROBOT.wait_start() # start the robot
    return

init()
print("Finished Running")