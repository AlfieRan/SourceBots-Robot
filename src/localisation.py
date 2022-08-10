from tokens import Token
from scoring_zones import Zones
from sbot import Robot
import math

# environment constants
DIST_BETWEEN_=0.675
NORTH_WALL=[i for i in range(0,7)]
EAST_WALL=[i for i in range(7,14)]
SOUTH_WALL=[i for i in range(14,21)]
WEST_WALL=[i for i in range(21,28)]
STARTING_BEARING=[2.35,-2.35,-0.785,0.785]
STARTING_POS=[(-2.2,2.2),(2.2,2.2),(-2.2,-2.2),(2.2,-2.2)]

class local:
    def __init__(self, robot: Robot):
        self.starting_zone = robot.zone
        self.x = STARTING_POS[self.starting_zone][0]
        self.y = STARTING_POS[self.starting_zone][1]
        self.team_tokens = robot.zone + 28
        self.bearing = STARTING_BEARING[self.starting_zone]
        self.ROBOT = robot
        self.ARDUINO = self.ROBOT.arduino
        self.CAMERA = robot.camera
        # TODO update this to not just be i
        self.tokens = [Token(posX=i, posY=i, id=i) for i in range(0,6)]

    def closest_non_zone_token(self):
        closest = {"token": None, "dist": 999}
        for token in self.tokens:
            dist_from = token.distance_from((self.x, self.y))
            if (dist_from < closest["dist"] and not Zones.check_in_zone(token.expected_x, token.expected_y)):
                closest = {"token": token, "dist": dist_from}
        
        return closest["token"]

    def last_checked_token(self):
        last_checked = {"token": None, "time": 0}
        for token in self.tokens:
            time_since = token.time_since_checked()
            if (time_since > last_checked["time"]):
                last_checked = {"token": token, "time": time_since}

        return (last_checked["token"], last_checked["time"])

    def furthest_forward_team_tokens(self, markers):
        tokens = []
        angle_tolerance = 0.5 # max deviation in radians
        dist_tolerance = 0.3

        for marker in markers:
            if marker.id == self.team_tokens and marker.spherical.rot_y < angle_tolerance:
                tokens.append(marker)

        distance = self.get_furthest(tokens)

        while distance > dist_tolerance:
            pass
        
    def get_furthest(self, markers):
        furthest = 0
        for marker in markers:
            if marker.distance > furthest:
                furthest = marker.distance

        return furthest

    def get_co_ords(self):
        # TODO - ideally make this work
        pass

    # def get_current_angle(self):
    #     curView = self.CAMERA.see()
    #     wall_markers = []

    #     for marker in curView.markers:
    #         if marker.id < 28:
    #             wall_markers.append(marker)

    # def get_bearing_using_marker(self, marker):
    #     angle_to_marker_wall = (math.pi/2) - (marker.spherical.rot_y + marker.orientation.rot_y)
    #     if marker.id in EAST_WALL:
    #         angle_to_marker_wall += (math.pi/2)
    #     elif marker.id in SOUTH_WALL:
    #         angle_to_marker_wall += 
    #     return 
