from sbot import Robot
import sensors

ROBOT = Robot(wait_start=False, debug=True) # create the robot object
SENSORS = sensors.Sensors(ROBOT)
ROBOT.wait_start()

while (True):
    if (SENSORS.check_right_collision()):
        ROBOT.motor_board.motors[0].power = 0
        ROBOT.motor_board.motors[1].power = 0
    else:
        ROBOT.motor_board.motors[0].power=0.2
        ROBOT.motor_board.motors[1].power=0.2