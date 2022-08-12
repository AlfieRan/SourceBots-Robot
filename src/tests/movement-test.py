import movement
from sbot import Robot
import time

ROBOT = Robot(debug=True) # create the robot object
MOVEMENT = movement.get_movement(ROBOT)
MOVEMENT.set_forward()
time.sleep(5)