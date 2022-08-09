from sbot import Robot
from sbot.env import ConsoleEnvironment, HardwareEnvironment
import movement
import time

# configuration constants - change these but not others unless you know what you're doing
TESTING=False

# code based constants - don't change these unless you know what you're doing
ENVIRONMENT = HardwareEnvironment if not TESTING else ConsoleEnvironment # environment to run in
ROBOT = Robot(wait_start=False, debug=True, ) # create the robot object
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

    test() # run the test function
    return


def test():
    print("Testing...")

    for i in range(0, 5):
        MOVEMENT.forward() # move forward
        time.sleep(1000)   # wait 1 second
        MOVEMENT.stop()  # stop
        time.sleep(1000)   # wait 1 second
        MOVEMENT.backward() # move backward
        time.sleep(1000)   # wait 1 second
        MOVEMENT.stop()  # stop
        time.sleep(1000)   # wait 1 second

    return

init()
print("Finished Running")