from sbot import Robot
import movement
import time

# constants - robot
ROBOT = Robot(wait_start=False) # create the robot object
ARDUINO = ROBOT.arduino     # get the arduino object
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

    for i in range(0, 50):
        MOVEMENT.forward() # move forward
        time.sleep(1000)   # wait 1 second
        MOVEMENT.backward() # move backward
        time.sleep(1000)   # wait 1 second

    return

init()
print("Finished Running")