from sbot import Robot
from sbot import BRAKE, COAST

# Constants
FLIP_MOTORS = False # if true, the motors are flipped - setting index 1 to 0 and index 0 to 1


class Motor:
    def __init__(self, index: int, ROBOT: Robot):
        self.ROBOT = ROBOT
        self.MOTOR = ROBOT.motor_board.motors[index]
        
    def forward(self, speed): # speed is a number between 0 and 100
        self.MOTOR.power = speed / 100
    
    def backward(self, speed):
        self.MOTOR.power = -speed / 100

    def stop(self):
        self.MOTOR.power = BRAKE

class Movement:
    defualt_turning_power = 15 # default power for motors
    defualt_speed = 20 # default speed for motors

    def __init__(self, motor_left: Motor, motor_right: Motor):
        # setup motors
        self.motor_left = motor_left
        self.motor_right = motor_right

    def forward(self, speed=defualt_speed):
        # put both motors forward at the same speed
        self.motor_left.forward(speed)
        self.motor_right.forward(speed)

    def backward(self, speed=defualt_speed):
        # put both motors backward at the same speed
        self.motor_left.backward(speed)
        self.motor_right.backward(speed)

    def turn_right(self, speed=defualt_turning_power):
        # set one motor to go forward and the other to go backward to turn right
        self.motor_left.forward(speed)
        self.motor_right.backward(speed)

    def turn_left(self, speed=defualt_turning_power):
        # set one motor to go backward and the other to go forward to turn left
        self.motor_left.backward(speed)
        self.motor_right.forward(speed)

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

def flip_inputs(index):
    flipped = {0: 1, 1: 0} # create a dictionary which contains the flipped index of the motors

    if FLIP_MOTORS: # if the motors are flipped, return the flipped index
        return flipped[index]
    
    return index # if the motors haven't been flipped then return the normal index

def get_movement(ROBOT: Robot):
    print("Creating movement object...")
    Motor_Left = Motor(flip_inputs(0), ROBOT)   # create the left motor object
    Motor_Right = Motor(flip_inputs(1), ROBOT)  # create the right motor object
    MOVEMENT = Movement(Motor_Left, Motor_Right)    # create the movement object
    return MOVEMENT # return the movement object
