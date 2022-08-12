from sbot import Robot
import sensors

ROBOT = Robot(wait_start=False, debug=True) # create the robot object
SENSORS = sensors.Sensors(ROBOT)
ROBOT.wait_start()

print(SENSORS.ultrasound_data)
