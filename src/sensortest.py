from sbot import Robot, GPIOPinMode
import time
import movement

TRIGGER_PIN=2
ECHO_PINS=[3,4,5]

ROBOT = Robot(wait_start=False, debug=True)
ARDUINO = ROBOT.arduino
MOVEMENT = movement.get_movement(ROBOT) # get the movement object

ARDUINO.pins[2].mode = GPIOPinMode.DIGITAL_OUTPUT
ARDUINO.pins[3,4,5].mode = GPIOPinMode.DIGITAL_INPUT

ULTRASOUND_SENSORS = []
for i in range(0,3):    
    ULTRASOUND_SENSORS.append(ARDUINO.ultrasound_sensors[TRIGGER_PIN, ECHO_PINS[i]])


start_time = int(time.time())
while (int(time.time() - start_time) < 15):
    obstacle = False

    for sensor in ULTRASOUND_SENSORS:
        if sensor.distance() < 0.2:
            obstacle = True
        
    if not obstacle:
        MOVEMENT.set_forward()
    else:
        MOVEMENT.stop()

