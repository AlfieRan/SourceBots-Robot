from sbot import Robot

TRIGGER_PIN=2
ECHO_PINS=[5,3,4]

class Sensors():
    def __init__(self, ROBOT: Robot):
        self.ROBOT = ROBOT
        self.ARDUINO = ROBOT.arduino
        self.COLLISION_TOLERANCE = 0.35
        # 0=left, 1=middle, 2=right

    def collision_checker_internal(self, dist):
        if dist == None:
            return False
        
        return dist < self.COLLISION_TOLERANCE

    def check_front_collision(self):
        dist = self.get_middle()
        return self.collision_checker_internal(dist)

    def check_left_collision(self):
        dist = self.get_left()
        return self.collision_checker_internal(dist)
    
    def check_right_collision(self):
        dist = self.get_right()
        return self.collision_checker_internal(dist)

    def get_left(self):
        return self.ARDUINO.ultrasound_sensors[TRIGGER_PIN, ECHO_PINS[0]].distance() 

    def get_middle(self):
        return self.ARDUINO.ultrasound_sensors[TRIGGER_PIN, ECHO_PINS[1]].distance() 

    def get_right(self):
        return self.ARDUINO.ultrasound_sensors[TRIGGER_PIN, ECHO_PINS[2]].distance() 