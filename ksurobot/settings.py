''' settings.py

    Define the settings to use for the robot and it's components
'''

try:
    import RPi.GPIO as io
except ImportError:
    io = None


##############################################################

# Server Setings
SERVER_IP = '129.130.46.4'
SERVER_PORT = 8055

##############################################################

# Servo settings
SERVO_I2C_ADDRESS = 0x40
SERVO_PWM_FREQ = 60

# Servo 0 settings
SERVO_0_CHANNEL = 0
SERVO_0_ON_BUTTON = 'r_bump'
SERVO_0_OFF_BUTTON = 'l_bump'
SERVO_0_MAX_PWM = 3000
SERVO_0_MIN_PWM = 1000
SERVO_0_SPEED = 300

# Servo 1 settings
SERVO_1_CHANNEL = 1
SERVO_1_ON_BUTTON = 'up'
SERVO_1_OFF_BUTTON = 'down'
SERVO_1_MAX_PWM = 3000
SERVO_1_MIN_PWM = 1000
SERVO_1_SPEED = 300

##############################################################

# Motor settings
MOTOR_I2C_ADDRESS = 0x40
MOTOR_PWM_FREQ = 1600

# Motor 0 settings
MOTOR_0_CHANNEL = 0
MOTOR_0_FORWARD_AXIS = 'r_trigger'
MOTOR_0_BACKWARD_AXIS = 'l_trigger'
MOTOR_0_DIR_PIN = 26
MOTOR_0_REVERSE = False

# Motor 1 settings
MOTOR_1_P1 = None
MOTOR_1_P2 = None
MOTOR_1_HIGH = None
MOTOR_1_LOW = None
MOTOR_1_REVERSE = None

# Motor 2 settings
MOTOR_2_P1 = None
MOTOR_2_P2 = None
MOTOR_2_HIGH = None
MOTOR_2_LOW = None
MOTOR_2_REVERSE = None

# Motor 3 settings
MOTOR_3_P1 = None
MOTOR_3_P2 = None
MOTOR_3_HIGH = None
MOTOR_3_LOW = None
MOTOR_3_REVERSE = None

##############################################################

# GPIO settings
if io:
    GPIO_MODE = io.BCM

# LED settings
LED_BUTTON = 'a'
LED_PIN = 20

##############################################################

SPI_DEVICE = 0

##############################################################

# Sensor 0 settings
SENSOR_0_NAME = 'Sensor 0'
SENSOR_0_CHANNEL = 0
SENSOR_0_COEFFICIENTS = []

# Sensor 1 settings
SENSOR_1_NAME = 'Sensor 1'
SENSOR_1_CHANNEL = 1
SENSOR_1_COEFFICIENTS = []

# Sensor 2 settings
SENSOR_2_NAME = 'Sensor 2'
SENSOR_2_CHANNEL = 2
SENSOR_2_COEFFICIENTS = []

# Sensor 3 settings
SENSOR_3_NAME = 'Sensor 3'
SENSOR_3_CHANNEL = 3
SENSOR_3_COEFFICIENTS = []

# Sensor 4 settings
SENSOR_4_NAME = 'Sensor 4'
SENSOR_4_CHANNEL = 4
SENSOR_4_COEFFICIENTS = []

# Sensor 5 settings
SENSOR_5_NAME = 'Sensor 5'
SENSOR_5_CHANNEL = 5
SENSOR_5_COEFFICIENTS = []

# Sensor 6 settings
SENSOR_6_NAME = 'Sensor 6'
SENSOR_6_CHANNEL = 6
SENSOR_6_COEFFICIENTS = []

# Sensor 7 settings
SENSOR_7_NAME = 'Sensor 7'
SENSOR_7_CHANNEL = 7
SENSOR_7_COEFFICIENTS = []

##############################################################
