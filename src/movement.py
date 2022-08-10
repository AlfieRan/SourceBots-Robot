from operator import index
from sbot import Robot, BRAKE, COAST
from localisation import Local
import math
from src.sensors import Sensors
import utils
import time

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
    angle_accuracy = 0.1  # min accuracy of angle in radians
    distance_accuracy = 0.3     # min distance to location in meters
    token_distance_accuracy = 0.15

    def __init__(self, motor_left: Motor, motor_right: Motor, ROBOT: Robot, TOKEN_ID: int):
        self.TOKEN_ID = TOKEN_ID
        self.ROBOT = ROBOT
        self.CAMERA = ROBOT.camera
        self.SENSORS = Sensors(ROBOT)
        # setup motors
        self.motor_left = motor_left
        self.motor_right = motor_right

    def goto_pos(self, x, y):
        while(utils.distance((Local.x, Local.y), (x,y))):
            self.lookat_pos(x,y)
            self.set_forward()
            print(f"Currently {utils.distance((Local.x, Local.y),(x,y))} from object")
        
    def goto_nearest_token(self):
        nearest_token = self.get_nearest_token()

        while (nearest_token.distance > self.token_distance_accuracy):
            self.lookat_nearest_token(nearest_token)
            avoided = self.collision_avoidance()

            if avoided:
                nearest_token = self.get_nearest_token
                self.lookat_nearest_token(nearest_token)

            self.set_forward()
            nearest_token = self.get_nearest_token()

    def collision_avoidance(self):
        if self.SENSORS.check_front_collision:
            time.sleep(100)

        if self.SENSORS.check_front_collision:
            self.set_turn_right()

            while self.SENSORS.check_front_collision:
                time.sleep(50)

            self.stop()
            return True

        return False

    def get_nearest_token(self):
        nearest_token = None

        while nearest_token == None:
            # TODO this currently only factors in tokens it can see and not all the tokens - intergrate expected co-ords for that
            for marker in self.CAMERA.see():
                if nearest_token == None:
                    nearest_token = marker
                elif marker.id == self.TOKEN_ID and marker.distance < nearest_token.distance:
                    nearest_token = marker

            if nearest_token == None:
                self.set_turn_right()
                time.sleep(50)
            else:
                return nearest_token
        
        return nearest_token

    def lookat_nearest_token(self, marker):
        while (utils.abs(marker.spherical.rot_y) > self.angle_accuracy):
            if (marker.spherical.rot_y > 0):
                # co-ord is on the right, hence turn right
                self.set_turn_right()
            else:
                # object is left so turn left 
                self.set_turn_left()

            marker = self.get_nearest_token()

        self.stop()

    def lookat_pos(self, x, y):
        # THIS DOES NOT WORK
        angle = 4
        while angle > self.angle_accuracy:
            angle = self.get_angle_radian(x, y)
        
        
        self.stop()
        # should now be looking at that location
        
    def get_angle_radian(self, x, y):
        # positive = right, negative = left
        difX = x - 0
        difY = y - 0
        ratio = difX/difY
        return math.atan(ratio)

    def set_forward(self, speed=defualt_speed):
        # put both motors forward at the same speed
        self.motor_left.forward(speed)
        self.motor_right.forward(speed)

    def set_backward(self, speed=defualt_speed):
        # put both motors backward at the same speed
        self.motor_left.backward(speed)
        self.motor_right.backward(speed)

    def set_turn_right(self, speed=defualt_turning_power):
        # set one motor to go forward and the other to go backward to turn right
        self.motor_left.forward(speed)
        self.motor_right.backward(speed)

    def set_turn_left(self, speed=defualt_turning_power):
        # set one motor to go backward and the other to go forward to turn left
        self.motor_left.backward(speed)
        self.motor_right.forward(speed)

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

    def sweep_collect(self):
        # TODO test this!!!!
        accuracy = 10
        turning_radius = 0.5
    
        for i in range(accuracy):
            self.set_forward()
            time.sleep(turning_radius/accuracy)
            self.set_turn_right()
            time.sleep(1/accuracy)
            self.stop()

def flip_inputs(index):
    flipped = {0: 1, 1: 0} # create a dictionary which contains the flipped index of the motors

    if FLIP_MOTORS: # if the motors are flipped, return the flipped index
        return flipped[index]
    
    return index # if the motors haven't been flipped then return the normal index

def get_movement(ROBOT: Robot, TOKEN_ID: int):
    print("Creating movement object...")
    Motor_Left = Motor(flip_inputs(0), ROBOT)   # create the left motor object
    Motor_Right = Motor(flip_inputs(1), ROBOT)  # create the right motor object
    MOVEMENT = Movement(Motor_Left, Motor_Right, ROBOT, TOKEN_ID)    # create the movement object
    return MOVEMENT # return the movement object

