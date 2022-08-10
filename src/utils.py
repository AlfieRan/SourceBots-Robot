import time
import math

def abs(inp):
    return max(inp, -inp)

def dif(a, b):
    return abs(a-b)

def distance(a, b):
    return math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))

def epoch_time(self):
        return int(time.time())