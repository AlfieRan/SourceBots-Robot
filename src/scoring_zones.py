import utils

class Scoring_Zones:
    def __init__(self):
        self.x = 0  # set the center of the scoring zone - using the (0,0) co-ord for this
        self.y = 0

        self.zone_width = 1 # m size of zone in each direction
        self.tape_width = 0.05 # m between zones (rounded up)
        self.tolerance = 0.05 # m tolerance per zone (x3 to get whole zone)

        self.unsafe = self.tolerance + self.tape_width
        self.zones = self.get_zones()
        self.variance = (self.zone_width*1.5) + self.tape_width

    def get_zones(self):
        return [[self.get_center(x,y) for x in range(0,3)] for y in range(2,-1,-1)]
        # the inverse for loops ensure that the [0,0]th item in the zones is the top left, [2,2]nd being bottom right, etc

    def get_center(self, x, y):
        output = []
        for point, center in zip([x, y], [self.x, self.y]):
            point -= self.zone_width # this ensures that the center point is not in the top left hand corner but rather the actual center
            
            # can't forget the tape!!
            if point < center:
                point -= self.tape_width
            elif point > center:
                point += self.tape_width

            output.append(point)

        # return the center point
        return (output[0], output[1])

    def get_variance(self):
        # this gets the variation of the inside of the outer zone and the center of the zones
        return (self.zone_width * 1.5) + self.unsafe

    def check_in_zone(self, x: float, y: float):
        # this checks if a set of co-ordinates are in a scoring zone and if so returns the zone

        if (utils.abs(x-self.x) > self.variance) or (utils.abs(y-self.y) > self.variance):
            # if the co-ord is outside the outer ring of the scoring zones then it's defintely not in a zone
            print(f"Co-ord: {(x,y)} is not in a zone")
            return False
        
        # figure out which y layer the co-ord is likely to be in 
        yLayer = {"layer": [], "index": 0}
        xLayer = {"layer": [], "index": 0}

        for i in range(len(self.zones)):
            zone_layer = self.zones[i]
            if utils.dif(y, zone_layer[0][1]) < (self.zone_width - self.tolerance) / 2:
                yLayer = {"layer": zone_layer, "index": i}


        # then figure out if the x co-ord is within one of those zones
        for i in range(len(yLayer["layer"])):
            zone = yLayer["layer"][i]
            if utils.dif(x, zone[0]) < (self.zone_width - self.tolerance) / 2:
                xLayer = {"layer": zone_layer, "index": i}

        zone_co_ord = (xLayer["index"], yLayer["index"])
        print(f"Co-ord: {(x,y)}\nZone: {zone_co_ord}")
        


        # Now need to implement a checker to ensure the bot is not on a white line, then return which zone it is in

    def get_all_good_points(self, accuracy):
        in_zone = []
        for x in range(-27*accuracy, 27*accuracy, 1):
            for y in range(-27*accuracy, 27*accuracy, 1):
                if Zones.check_in_zone(x/10*accuracy,y/10*accuracy) != False:
                    in_zone.append((x/10*accuracy,y/10*accuracy))

        print("\n\n\n\n Co-ords in zones are:")
        print(in_zone)

Zones = Scoring_Zones()