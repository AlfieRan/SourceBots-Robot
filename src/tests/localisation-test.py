import localisation
from sbot import Robot

ROBOT = Robot()
LOCAL = localisation.local(ROBOT)

print("Getting location....")
print(LOCAL.get_co_ords())