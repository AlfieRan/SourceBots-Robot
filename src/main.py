# --------------- LICENSE ---------------
# Some or all of this code was originally created by Alfie Ranstead
# https://github.com/alfieran or alfie.ranstead@outlook.com
# During August 2022 for the Sourcebots Southampton University Competition
# If you would like to use this code if your own projects please read the license:
# https://github.com/AlfieRan/SourceBots-Robot
# ------------- END LICENSE -------------


from random import random
from sbot import Robot
import localisation
import movement
import time
import utils
import sensors
import random


ROBOT = Robot(debug=True) # create the robot object
ARDUINO = ROBOT.arduino     # get the arduino object
TOKEN_ID = ROBOT.zone + 28
LOCAL = localisation.local(ROBOT)
MOVEMENT = movement.get_movement(ROBOT, LOCAL=LOCAL, TOKEN_ID=TOKEN_ID) # get the movement object
SENSORS = sensors.Sensors(ROBOT)

def get_tokens_from_markers(markers):
    tokens = []

    print("checking for tokens in markers")
    for marker in markers:
        if marker.id == TOKEN_ID:
            tokens.append(marker)

    print("finished checking for tokens")
    return tokens

def dumb_start():
    MOVEMENT.set_forward()
    time.sleep(2)
    MOVEMENT.set_turn_left()
    time.sleep(0.1)
    MOVEMENT.set_forward()
    time.sleep(1)
    MOVEMENT.stop()
    MOVEMENT.set_turn_left()
    time.sleep(0.7)
    MOVEMENT.set_forward()
    time.sleep(2)
    MOVEMENT.stop()
    MOVEMENT.set_backward()
    time.sleep(2)
    MOVEMENT.set_turn_left()
    time.sleep(2)
    MOVEMENT.stop()

def start():
     # position right, go forward until collected 3 tokens
    img_markers = ROBOT.camera.see()
    tokens = get_tokens_from_markers(img_markers)
    print(f"Collecting tokens: {tokens}")
    MOVEMENT.set_forward(20)

    while (len(tokens) > 0):
        print("going to tokens")
        MOVEMENT.set_forward(20)
        time.sleep(0.5)
        MOVEMENT.stop_instantly()
        print("stopping")
        img_markers = ROBOT.camera.see()
        tokens = get_tokens_from_markers(img_markers)
        print("rescanning tokens")

        # adjust to angle variations
        print("look at token")
        closest = LOCAL.get_closest_token(tokens)
        if closest == None:
            print("no more tokens, breaking out of start loop")
            break

        print("got closest tokens")
        if closest.spherical.rot_y > 0.1:
            print("rotating right to look at them properly")
            MOVEMENT.set_turn_right(10)
            time.sleep(0.1)
            MOVEMENT.stop()
        elif closest.spherical.rot_y < 0.1:
            print("rotating left to target token")
            MOVEMENT.set_turn_left(10)
            time.sleep(0.1)
            MOVEMENT.stop()
        print("should be looking at token now")


    MOVEMENT.set_forward(20)
    time.sleep(0.5)

    print("pushing tokens to main zone")
    # MOVEMENT.stop()
    # print("Stopped")
    # MOVEMENT.set_turn_left()
    # print("turning left")
    # time.sleep(0.5)
    # MOVEMENT.stop()
    # print("going forward")
    # MOVEMENT.set_forward()
    # time.sleep(1.5)
    # MOVEMENT.stop()
    # MOVEMENT.set_backward(20)
    # time.sleep(1.5)
    # MOVEMENT.set_turn_left()
    # time.sleep(0.5)
    MOVEMENT.push_to_center()
    return

def default():
    # go to nearest token
    print("Going to nearest token")
    MOVEMENT.goto_nearest_token()
     # check if the token is already in the scoring zone
    in_zone = LOCAL.in_zone()
    if (in_zone):
        print("currently in a zone so dip")()
        MOVEMENT.move_out()
        MOVEMENT.stop()
    else:
        print("currently not in a zone so collect the token and push it into a zone")
        # collect token 
        MOVEMENT.set_forward(20)
        time.sleep(0.7)
        MOVEMENT.stop()
        print("should have collected the token")
                # go to roughly the center of the map
        print("pushing it to the center")
                # MOVEMENT.push_to_center()
        right_dist = SENSORS.get_right()
        left_dist = SENSORS.get_left()
        if (right_dist < left_dist):
                    MOVEMENT.set_turn_left()
                    time.sleep(1)
        else:
                    MOVEMENT.set_turn_right()
                    time.sleep(1)
        MOVEMENT.set_forward()
        time.sleep(2)
        MOVEMENT.set_backward()
        time.sleep(2)
        MOVEMENT.set_turn_left()
        time.sleep(1)
                # stop moving
        print("stopping and restarting cycle")
        MOVEMENT.stop()

def main():
    Running = True
    # MOVEMENT.push_to_center()
    ### game plan
   
    # go left, dump them in the first zone
    # turn left and go forward a bit

    # loop:
    print("Entering main loop")
    while Running:
        try:
            if (SENSORS.check_front_collision()):
                if (SENSORS.check_left_collision() and not SENSORS.check_right_collision()):
                    MOVEMENT.set_turn_right()
                    time.sleep(1)
                    MOVEMENT.stop()
                elif (SENSORS.check_right_collision() and not SENSORS.check_left_collision()):
                    MOVEMENT.set_turn_left()
                    time.sleep(1)
                    MOVEMENT.stop()
                else:
                    if (random.randint(0,1) == 0):
                        MOVEMENT.set_turn_right()
                    else:
                        MOVEMENT.set_turn_left()

            elif (SENSORS.get_middle() > 1.2 and SENSORS.get_left() > 1.2 and SENSORS.get_right() > 1.2):
                MOVEMENT.set_backward()
                time.sleep(1.5)
                MOVEMENT.set_turn_left()
                time.sleep(1.5)
                MOVEMENT.set_forward()
                time.sleep(1.5)
                MOVEMENT.stop()

            else:
                default()

        except Exception as e:
            print("crased with erorr", e)
            default()


            

try:
    dumb_start()
except Exception as e:
    print("Start setup failed")
    print("error:", e)

while True:
    try:
        main()
    except Exception as e:
        print("main loop failed, restarting")
        print("error:", e)

print("Finished Running")