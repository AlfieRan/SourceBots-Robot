import time
import math

def abs(inp):
    return max(inp, -inp)

def dif(a, b):
    return abs(a-b)

def distance(a, b):
    return math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))

def epoch_time():
        return int(time.time())

def time_since(time):
    return epoch_time() - time

def get_intersections(pos0, r0, pos1, r1, max_variance=2.7):
    x0 = pos0[0]
    y0 = pos0[1]
    x1 = pos1[0]
    y1 = pos1[1]
    dist = distance(pos0, pos1)

    if dist > r0 + r1:
        # circles don't intersect
        return None

    elif dist < abs(r0-r1):
        # one circle is inside the other
        return None

    elif dist == 0 and r0 == r1:
        # circles are identical
        return None

    else:
        a = (r0**2-r1**2+dist**2) / (2*dist)
        h = math.sqrt(r0**2-a**2)
        x2 = x0 + a*(x1-x0)/dist
        y2 = y0 + a*(y1-y0)/dist

        x3 = x2 + h * (y1 - y0)/dist
        y3 = y2 - h * (x1 - x0)/dist
        x4 = x2-h*(y1-y0)/dist
        y4=y2+h*(x1-x0)/dist

        Intersections = [(x3, y3), (x4, y4)]
        valid_Intersections = []

        for intersection in Intersections:
            if intersection[0] < max_variance and intersection[1] < max_variance:
                valid_Intersections.append(intersection)

        if len(valid_Intersections) == 0:
            return None
        elif len(valid_Intersections) > 1 and valid_Intersections[0] != valid_Intersections[1]:
            print(f"WARNING - TWO VALID INTERSECTIONS FOUND - PROBABLY A LOGIC ERROR\n{valid_Intersections}")

        print(f"Intersection:\t{valid_Intersections[0]}")
        return valid_Intersections[0]
