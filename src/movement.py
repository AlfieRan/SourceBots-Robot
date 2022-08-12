from sbot import Robot, BRAKE, COAST
import math
from sensors import Sensors
import utils
import time

# Constants
FLIP_MOTORS = False # if true, the motors are flipped - setting index 1 to 0 and index 0 to 1
COMPENSATION = 0.9 # amount to turn right wheel by

class Motor:
    def __init__(self, index: int, ROBOT: Robot):
        self.ROBOT = ROBOT
        self.MOTOR = ROBOT.motor_board.motors[index]
        
    def forward(self, speed): # speed is a number between 0 and 100
        self.MOTOR.power = -speed / 100
    
    def backward(self, speed):
        self.MOTOR.power = speed / 100

    def stop(self):
        self.MOTOR.power = BRAKE

    def coast(self):
        self.MOTOR.power = COAST

class Movement:
    defualt_turning_power = 20 # default power for motors
    defualt_speed = 50 # default speed for motors
    angle_accuracy = 0.1  # min accuracy of angle in radians
    distance_accuracy = 0.3     # min distance to location in meters
    token_distance_accuracy = 0.15

    def __init__(self, motor_left: Motor, motor_right: Motor, ROBOT: Robot, LOCAL, TOKEN_ID=None):
        self.ROBOT = ROBOT
        self.CAMERA = ROBOT.camera
        self.SENSORS = Sensors(ROBOT)
        self.LOCAL = LOCAL

        if TOKEN_ID != None:
            self.TOKEN_ID = TOKEN_ID
        else:
            self.TOKEN_ID = 28 + ROBOT.zone
        # setup motors
        self.motor_left = motor_left
        self.motor_right = motor_right

    def goto_pos(self, x, y):
        Local = self.LOCAL.get
        while(utils.distance((Local.x, Local.y), (x,y)) > 500):
            self.lookat_pos(x,y)
            self.set_forward()
            print(f"Currently {utils.distance((Local.x, Local.y),(x,y))} from object")

        self.set_forward(20)
        time.sleep(1)
        
    def goto_nearest_token(self):
        nearest_token = self.get_nearest_token()
        print("Going to token {nearest_token.distance} away")

        while (nearest_token.distance > self.token_distance_accuracy):
            print("Started looking at nearest token")
            self.lookat_nearest_token()
            # avoided = self.collision_avoidance()
            print(f"Looking at nearest token.")

            # if avoided:
            #     nearest_token = self.get_nearest_token()
            #     self.lookat_nearest_token()

            print("Moving towards nearest token")
            self.set_forward()
            time.sleep(0.3)
            self.stop()
            refreshed_token = self.get_nearest_token()
            
            print("Token distance =", refreshed_token.distance)

            if refreshed_token.distance > 500:
                nearest_token = refreshed_token
            else:
                self.set_forward()
                time.sleep(0.2)
                self.stop()
                print("Finished getting token")
                break

    def collision_avoidance(self):
        if self.SENSORS.check_front_collision:
            time.sleep(0.5)

        if self.SENSORS.check_front_collision:
            self.set_turn_right()

            while self.SENSORS.check_front_collision:
                time.sleep(0.5)

            self.stop()
            return True

        return False

    def get_nearest_token(self):
        print("Finding nearest token")
        nearest_token = None

        while nearest_token == None:
            print("Looking for tokens...")
            # TODO this currently only factors in tokens it can see and not all the tokens - intergrate expected co-ords for that
            for marker in self.CAMERA.see():
                print(f"Checking marker with id {marker.id}")

                if nearest_token == None and marker.id == self.TOKEN_ID:
                    nearest_token = marker
                elif marker.id == self.TOKEN_ID and marker.distance < nearest_token.distance:
                    nearest_token = marker

            if nearest_token == None:
                print("No token detected, rotating")
                self.set_turn_right()
                time.sleep(0.1)
                self.stop()
                time.sleep(0.2)
            else:
                return nearest_token
        
        return nearest_token

    def lookat_nearest_token(self):
        marker = self.get_nearest_token()
        while (utils.abs(marker.spherical.rot_y) > self.angle_accuracy):
            if (marker.spherical.rot_y > 0):
                # co-ord is on the right, hence turn right
                self.set_turn_right()
                time.sleep(0.05)
                self.stop()
                time.sleep(0.1)
            else:
                # object is left so turn left 
                self.set_turn_left()
                time.sleep(0.05)
                self.stop()
                time.sleep(0.1)

            marker = self.get_nearest_token()

        self.stop()

    def lookat_pos(self, x, y):
        print("Looking at position started")
        angle = 4
        local_angle = self.LOCAL.get_angle()
        while abs(angle - local_angle) > self.angle_accuracy:
            angle = self.get_angle_to_pos(x, y)
            print(f"Current angle to {(x,y)} is {angle} radians")

            if (angle - local_angle) > 0:
                print("turning right")
                self.set_turn_right(10)
            else:
                print("turning left")
                self.set_turn_left(10)
            
            time.sleep(0.3)
            self.stop()
            print("finished turning")

            local_angle = self.LOCAL.get_angle()
            angle = self.get_angle_to_pos(x,y)

        print(f"Now at angle: {angle} to {(x,y)}")
        
        self.stop()
        # should now be looking at that location

    def move_out(self):
        # get out the way of current blocks
        print("Moving away from nearby blocks")
        self.set_backward(20)
        time.sleep(1.5)
        self.stop()
        self.set_turn_left()
        time.sleep(1)
        self.set_forward(20)
        time.sleep(1)
        self.stop()
        print("finished moving away")

    def get_angle_to_pos(self, x, y):
        local = self.LOCAL.get_co_ords()
        return math.atan((x-local[0])/(y-local[1]))

    def set_forward(self, speed=defualt_speed):
        # put both motors forward at the same speed
        self.motor_left.forward(speed)
        self.motor_right.forward(speed*COMPENSATION)

    def set_backward(self, speed=defualt_speed):
        # put both motors backward at the same speed
        self.motor_left.backward(speed)
        self.motor_right.backward(speed*COMPENSATION)

    def set_turn_right(self, speed=defualt_turning_power):
        # set one motor to go forward and the other to go backward to turn right
        self.motor_left.forward(speed)
        self.motor_right.backward(speed*COMPENSATION)

    def set_turn_left(self, speed=defualt_turning_power):
        # set one motor to go backward and the other to go forward to turn left
        self.motor_left.backward(speed)
        self.motor_right.forward(speed*COMPENSATION)

    def push_to_center(self):
        print("Starting to push tokens to center")
        start_time = utils.epoch_time()
        cur_time = utils.epoch_time()

        while (not self.LOCAL.in_zone() and cur_time - start_time < 25):
            collision_forward = self.SENSORS.check_front_collision()
            print(f"currently in scoring zone: {self.LOCAL.in_zone()}")
            print(f"time at: {cur_time - start_time}")

            if not collision_forward:
                print("No forward obstacles, move towards center")
                self.set_turn_left()
                time.sleep(1)
                self.stop()
                print("Manual override movement setup just in case")
                self.lookat_pos(0,0)
                self.set_forward(20)
            else:
                print(f"deteched a forward collision")
                collision_forward = self.check_front_collision()

                while (collision_forward):
                    print("Turning left to avoid collision")
                    self.set_turn_left()
                    time.sleep(0.5)
                    self.stop()
                    print("finished turning left, rechecking for collisions")
                    collision_forward = self.check_front_collision()
                
                print("Now out of the way of collisions")
                self.set_forward(30)
                time.sleep(0.5)
                self.stop()
                print("Should now be gone around collision")
            
            
            cur_time = utils.epoch_time()

        print("Left tokens in center, moving away")
        print(f"time taken: {cur_time - start_time}")
        self.move_out()

    def stop(self):
        print("Stopping")
        self.set_forward(25)
        time.sleep(0.1)
        self.motor_left.stop()
        self.motor_right.stop()
        print("Stopped")

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

def get_movement(ROBOT: Robot, LOCAL, TOKEN_ID=None):
    print("Creating movement object...")
    Motor_Left = Motor(flip_inputs(0), ROBOT)   # create the left motor object
    Motor_Right = Motor(flip_inputs(1), ROBOT)  # create the right motor object
    MOVEMENT = Movement(Motor_Left, Motor_Right, ROBOT, LOCAL, TOKEN_ID)    # create the movement object
    return MOVEMENT # return the movement object

