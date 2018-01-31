''' Robot.py

    Describe what components the robot is made of
'''

from Components import *
from Settings import *


class Robot(object):

    def __init__(self):

        # Setup drive motors
        self.drive_motor_0 = DCMotorComponent(
            DRIVE_MOTOR_0_P1,
            DRIVE_MOTOR_0_P2,
            DRIVE_MOTOR_0_HIGH,
            DRIVE_MOTOR_0_LOW,
            reverse=DRIVE_MOTOR_0_REVERSE
        )

        self.drive_motor_1 = DCMotorComponent(
            DRIVE_MOTOR_1_P1,
            DRIVE_MOTOR_1_P2,
            DRIVE_MOTOR_1_HIGH,
            DRIVE_MOTOR_1_LOW,
            reverse=DRIVE_MOTOR_1_REVERSE
        )

        # Setup drive motors
        self.front_led_0 = LEDComponent(
            LED_0_BUTTON,
            LED_0_PIN
        )

        self.front_led_1 = LEDComponent(
            LED_1_BUTTON,
            LED_1_PIN
        )

        # Setup sensors
        self.sensor_0 = SensorComponent(
            SENSOR_0_PIN,
            SENSOR_0_CHANNEL
        )

        self.sensor_1 = SensorComponent(
            SENSOR_1_PIN,
            SENSOR_1_CHANNEL
        )

        self.sensor_2 = SensorComponent(
            SENSOR_2_PIN,
            SENSOR_2_CHANNEL
        )

        self.sensor_3 = SensorComponent(
            SENSOR_3_PIN,
            SENSOR_3_CHANNEL
        )

        # Setup steering motors
        self.steer_motor_0 = DCMotorComponent(
            STEER_MOTOR_0_P1,
            STEER_MOTOR_0_P2,
            STEER_MOTOR_0_HIGH,
            STEER_MOTOR_0_LOW,
            reverse=STEER_MOTOR_0_REVERSE
        )

        self.steer_motor_1 = DCMotorComponent(
            STEER_MOTOR_1_P1,
            STEER_MOTOR_1_P2,
            STEER_MOTOR_1_HIGH,
            STEER_MOTOR_1_LOW,
            reverse=STEER_MOTOR_1_REVERSE
        )
    
    def get_msg(self):
        pass
    
    def stop(self):
        pass
    
    def update(self):
        pass
