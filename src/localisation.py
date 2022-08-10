from tokens import Token
from scoring_zones import Zones

class local:
    def __init__(self, starting_x=0, starting_y=0, starting_bearing=0):
        self.x = starting_x
        self.y = starting_y
        self.bearing = starting_bearing
        # TODO starting positions should be according to the rules, not i
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

Local = local() # TODO feed starting co-ords and bearing based upon the rules