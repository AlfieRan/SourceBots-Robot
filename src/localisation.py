# from tokens import Token
from scoring_zones import Zones
from sbot import Robot
import scoring_zones
import utils
import math

# environment constants
DIST_BETWEEN_=0.675
NORTH_WALL=[i for i in range(0,7)]
EAST_WALL=[i for i in range(7,14)]
SOUTH_WALL=[i for i in range(14,21)]
WEST_WALL=[i for i in range(21,28)]
STARTING_BEARING=[2.35,-2.35,-0.785,0.785]
STARTING_POS=[(-2.2,2.2),(2.2,2.2),(-2.2,-2.2),(2.2,-2.2)]

# top left = (-2.7, 2.7)
# split = 0.675
WALL_MARKER_CO_ORDS_NORTH = [((i*0.675)-2.7, 2.7) for i in range(1,8)]  # wall markers 0 -> 6
WALL_MARKER_CO_ORDS_EAST = [(2.7, i) for i in range(1,8)] # markers 7 -> 13
WALL_MARKER_CO_ORDS_SOUTH = [(2.7-(i*0.675), -2.7) for i in range(1,8)] # 14 -> 20
WALL_MARKER_CO_ORDS_WEST = [(-2.7, -2.7+(i*0.675)) for i in range(1,8)] # 21 -> 28

WALL_MARKER_CO_ORDS = WALL_MARKER_CO_ORDS_NORTH + WALL_MARKER_CO_ORDS_EAST + WALL_MARKER_CO_ORDS_SOUTH + WALL_MARKER_CO_ORDS_WEST

class local:
    def __init__(self, robot: Robot):
        self.starting_zone = robot.zone
        self.x = STARTING_POS[self.starting_zone][0]
        self.y = STARTING_POS[self.starting_zone][1]
        self.ZONES = scoring_zones.Zones
        self.team_tokens = robot.zone + 28
        self.bearing = STARTING_BEARING[self.starting_zone]
        self.ROBOT = robot
        self.ARDUINO = self.ROBOT.arduino
        self.CAMERA = robot.camera
        # TODO update this to not just be i
        # self.tokens = [Token(posX=i, posY=i, id=i) for i in range(0,6)]   

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

    def get_angle(self):
        # todo MAKE THIS WORK
        markers = self.CAMERA.see()
        best = None
        for marker in markers:
            if marker.id < 28:
                if best == None or best.spherical.rot_y > marker.spherical.rot_y:
                    best = marker
      
        if best == None:
            return self.bearing

        additional = 0

        if marker.id > 6 and marker.id < 14:
            additional = math.pi/2
        elif marker.id > 13 and marker.id < 21:
            if self.bearing > 0:
                additional = -math.pi
            else:
                additional = math.pi
        elif marker.id > 20:
            additional = -math.pi/2
        
        bearing = best.spherical.rot_y + additional
        self.bearing = bearing
        return bearing

    def get_co_ords(self):
        self.ROBOT.motor_board.motors[0].power = 0
        self.ROBOT.motor_board.motors[1].power = 0
        markers = self.CAMERA.see()
        walls = []
        best_dir = None

        for marker in markers:
            if marker.id < 28:
                walls.append(marker)
                if best_dir == None:
                    best_dir = marker
                elif best_dir.spherical.rot_y > marker.spherical.rot_y:
                    best_dir = marker

        co_ords = WALL_MARKER_CO_ORDS[best_dir.id]
        rot = best_dir.spherical.rot_y
        dist = best_dir.distance
        return (co_ords[0]-(dist * math.sin(rot)),co_ords[1]-(dist * math.cos(rot)))

            
    def get_closest_token(self, tokens):
        closest = tokens[0]
        dist = 999

        for token in tokens:
            if token.distance < dist:
                dist = token.distance
                closest = token
        
        return closest

    def in_zone(self):
        pos = self.get_co_ords()
        return (self.ZONES.check_in_zone(pos[0], pos[1]) != False)

    def get_co_ords_old(self):
        markers = self.CAMERA.see()
        self.CAMERA.save("vision.jpg")
        walls = []
        co_ords = []
        avg = (0,0)

        for marker in markers:
            if marker.id < 28:
                walls.append(marker)

        if len(markers) < 2:
            return False

        print(f"Walls: {walls}")
        if len(walls):
            print("Only detected one wall")
            return (self.x, self.y)

        for wall_marker in walls:
            pair = self.get_pair(walls, wall_marker)
            print(f"Pairing walls: {wall_marker.id} and {pair.id}")
            expected_co_ord = utils.get_intersections(WALL_MARKER_CO_ORDS[wall_marker.id], wall_marker.distance, WALL_MARKER_CO_ORDS[pair.id], pair.distance)
            print(f"expected: {expected_co_ord}")
            if expected_co_ord != None:
                co_ords.append(expected_co_ord)

        print(f"co-ords, {co_ords}")

        for co_ord in co_ords:
            avg[0] += co_ord[0] / len(co_ords)
            avg[1] += co_ord[1] / len(co_ords)

        self.x = avg[0]
        self.y = avg[0]
        return avg



    def get_pair(self, markers, marker):
        other_markers = []
        pair_id = marker.id + 1

        for m in markers:
            if m.id == pair_id:
                return m
            elif m.id != marker.id:
                other_markers.append(m)

        return other_markers[0]



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
