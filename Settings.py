''' Settings.py

    Define the settings to use for the robot and it's components
'''

import RPi.GPIO as io

# Server Setings
SERVER_IP = '129.130.46.4'
SERVER_PORT = 8055

# Motor settings
MOTOR_PWM_FREQ = 1600

# Drive Motor 0 settings
DRIVE_MOTOR_0_P1 = None
DRIVE_MOTOR_0_P2 = None
DRIVE_MOTOR_0_HIGH = None
DRIVE_MOTOR_0_LOW = None
DRIVE_MOTOR_0_REVERSE = None

# Drive Motor 1 settings
DRIVE_MOTOR_1_P1 = None
DRIVE_MOTOR_1_P2 = None
DRIVE_MOTOR_1_HIGH = None
DRIVE_MOTOR_1_LOW = None
DRIVE_MOTOR_1_REVERSE = None

# Servo settings
SERVO_PWM_FREQ = 60

# LED/GPIO settings
GPIO_MODE = io.BCM

# LED 0 settings
LED_0_BUTTON = 'a'
LED_0_PIN = 20

# Sensor 0 settings
SENSOR_0_PIN = None
SENSOR_0_CHANNEL = None

# Sensor 1 settings
SENSOR_1_PIN = None
SENSOR_1_CHANNEL = None

# Sensor 2 settings
SENSOR_2_PIN = None
SENSOR_2_CHANNEL = None

# Sensor 3 settings
SENSOR_3_PIN = None
SENSOR_3_CHANNEL = None

