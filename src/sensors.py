from sbot import Robot
import utils

TRIGGER_PIN=2
ECHO_PINS=[3,4,5]

class Sensors():
    def __init__(self, ROBOT: Robot):
        self.ROBOT = ROBOT
        self.ARDUINO = ROBOT.arduino
        self.COLLISION_TOLERANCE = 0.35

        self.ultrasounds = [self.ARDUINO.ultrasound_sensors[TRIGGER_PIN, ECHO_PINS[i]] for i in range(0,3)]
        self.ultrasound_data = [self.ultrasounds[i].distance for i in range(0,3)]
        self.ultrasound_last_updated = utils.epoch_time()
        # 0=left, 1=middle, 2=right

    def get_all(self):
        self.ultrasound_data = []

        for ultrasound in self.ultrasounds:
            self.ultrasound_data.append(ultrasound.distance)

        self.ultrasound_last_updated = utils.epoch_time

    def check_front_collision(self):
        return self.get_middle() < self.COLLISION_TOLERANCE

    def check_left_collision(self):
        return self.get_left() < self.COLLISION_TOLERANCE
    
    def check_right_collision(self):
        return self.get_right() < self.COLLISION_TOLERANCE

    def get_left(self):
        self.get_all()
        return self.ultrasound_data[0]

    def get_middle(self):
        self.get_all()
        return self.ultrasound_data[1]

    def get_right(self):
        self.get_all()
        return self.ultrasound_data[2]