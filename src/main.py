from sbot import Robot
import localisation
import movement
import time
import utils
import sensors


ROBOT = Robot(debug=True) # create the robot object
ARDUINO = ROBOT.arduino     # get the arduino object
TOKEN_ID = 31 # ROBOT.zone + 28
LOCAL = localisation.local(ROBOT)
MOVEMENT = movement.get_movement(ROBOT, LOCAL=LOCAL, TOKEN_ID=TOKEN_ID) # get the movement object
SENSORS = sensors.Sensors(ROBOT)

def get_tokens_from_markers(markers):
    tokens = []

    for marker in markers:
        if marker.id == TOKEN_ID:
            tokens.append(marker)

    return tokens

def start():
     # position right, go forward until collected 3 tokens
    img_markers = ROBOT.camera.see()
    tokens = get_tokens_from_markers(img_markers)
    print(f"Collecting tokens: {tokens}")
    MOVEMENT.set_forward(20)

    while (len(tokens) > 0):
        MOVEMENT.set_forward(20)
        time.sleep(0.5)
        MOVEMENT.stop()
        img_markers = ROBOT.camera.see()
        tokens = get_tokens_from_markers(img_markers)

        # adjust to angle variations
        closest = LOCAL.get_closest_token(tokens)
        if closest.spherical.rot_y > 0.1:
            MOVEMENT.set_turn_right(10)
            time.sleep(0.1)
            MOVEMENT.stop()
        elif closest.spherical.rot_y < 0.1:
            MOVEMENT.set_turn_left(10)
            time.sleep(0.1)
            MOVEMENT.stop()


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

def main():
    Running = True
    ### game plan
   
    # go left, dump them in the first zone
    # turn left and go forward a bit

    # loop:
    print("Entering main loop")
    while Running:
        # go to nearest token
        print("Going to nearest token")
        MOVEMENT.goto_nearest_token()
        # check if the token is already in the scoring zone
        if (LOCAL.in_zone()):
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
            MOVEMENT.push_to_center()
            # stop moving
            print("stopping and restarting cycle")
            MOVEMENT.stop()

try:
    start()
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