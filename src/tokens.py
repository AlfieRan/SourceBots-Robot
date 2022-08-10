import math
import utils
from scoring_zones import Zones

class Token:
    def __init__(self, posX, posY, id):
        self.id = id
        self.expected_x = posX
        self.expected_y = posY
        self.last_updated = utils.epoch_time()

    def distance_from(self, pos: tuple(float)):
        return math.sqrt(((pos[0] - self.expected_x)**2) + ((pos[1] - self.expected_y)**2))

    def time_since_checked(self):
        return utils.epoch_time() - self.last_updated

    def in_zone(self):
        in_zone = Zones.check_in_zone(self.expected_x, self.expected_y)
        if (in_zone != False):
            return True
        return False
