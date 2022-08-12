import movement
from sbot import Robot

ROBOT = Robot(debug=True) # create the robot object
MOVEMENT = movement.get_movement(ROBOT)
while (True):
    MOVEMENT.goto_nearest_token()