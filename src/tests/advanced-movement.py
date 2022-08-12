import movement
from sbot import Robot

ROBOT = Robot(debug=True) # create the robot object
MOVEMENT = movement.get_movement(ROBOT)
print("going to nearest token")
MOVEMENT.goto_nearest_token()