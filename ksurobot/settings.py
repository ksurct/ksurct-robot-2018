''' settings.py

    Define the settings to use for the robot and it's components
'''

try:
    import RPi.GPIO as io
except RuntimeError:
    io = None


##############################################################

# Server Setings
SERVER_IP = '10.135.79.79'
SERVER_PORT = 8055

##############################################################

# Servo settings
SERVO_I2C_ADDRESS = 0x40 # Needs to be set
SERVO_PWM_FREQ = 60

# Servo 0 settings (Brontosaurus neck)
SERVO_0_CHANNEL = 0
SERVO_0_MODIFIER = 'l_bump'
SERVO_0_MAX_PWM = 4096
SERVO_0_MIN_PWM = 0
SERVO_0_PRESETS = [('y', 4096), ('a', 0)]
SERVO_0_CONTROL_SPEED = 1
SERVO_0_SPEED = 300

# Servo 1 settings (Front Wrist)
SERVO_1_CHANNEL = 1
SERVO_1_MODIFIER = None
SERVO_1_MAX_PWM = 4096
SERVO_1_MIN_PWM = 0
SERVO_1_PRESETS = [('y', 4096), ('x', 2048), ('a', 0)]
SERVO_1_CONTROL_SPEED = 1
SERVO_1_SPEED = 300

# Servo 2 settings (Claw)
SERVO_2_CHANNEL = 3 # 3 isn't a typo, Isaiah wired it dumbly
SERVO_2_MODIFIER = 'r_bump'
SERVO_2_MAX_PWM = 4096
SERVO_2_MIN_PWM = 0
SERVO_2_PRESETS = [('y', 4096), ('a', 0)]
SERVO_2_CONTROL_SPEED = 1
SERVO_2_SPEED = 300

##############################################################

# Motor settings
MOTOR_I2C_ADDRESS = 0x40 # Needs to be set
MOTOR_PWM_FREQ = 1000
MOTOR_TICKS_PER_ROTATE = 0 # this is not right, update after experiment

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
SENSOR_0_COEFFICIENTS = [-1.4874e-009,3.3770e-007,-3.3369e-005,1.8817e-003,-6.6700e-002,1.5423e+000,-2.3334e+001,2.2456e+002,-1.2740e+003,3.4590e+003,-5.5167e+002]

# Sensor 1 settings
SENSOR_1_NAME = 'Sensor 1'
SENSOR_1_CHANNEL = 1
SENSOR_1_COEFFICIENTS = [-2.7782e-009 , 6.1500e-007 , -5.8956e-005 , 3.2058e-003  ,-1.0879e-001 , 2.3874e+000  ,-3.3946e+001  ,3.0396e+002  ,-1.5929e+003 ,4.0159e+003,  -8.7167e+002]

# Sensor 2 settings
SENSOR_2_NAME = 'Sensor 2'
SENSOR_2_CHANNEL = 2
SENSOR_2_COEFFICIENTS = [ -2.7947e-009 , 6.1743e-007 , -5.9076e-005 , 3.2067e-003  ,-1.0865e-001 , 2.3810e+000  ,-3.3806e+001  ,3.0213e+002 ,-1.5781e+003 , 3.9496e+003,  -7.7006e+002]

# Sensor 3 settings
SENSOR_3_NAME = 'Sensor 3'
SENSOR_3_CHANNEL = 3
SENSOR_3_COEFFICIENTS = [-2.8357e-009,  6.2740e-007,  -6.0130e-005 , 3.2706e-003 , -1.1110e-001  ,2.4429e+000 , -3.4845e+001  ,3.1333e+002 ,-1.6505e+003 , 4.1942e+003 , -1.0622e+003]

# Sensor 4 settings
SENSOR_4_NAME = 'Sensor 4'
SENSOR_4_CHANNEL = 4
SENSOR_4_COEFFICIENTS = [ -1.5220e-009 , 3.4723e-007 , -3.4446e-005 , 1.9471e-003 , -6.9034e-002 , 1.5916e+000 , -2.3910e+001 , 2.2734e+002, -1.2683e+003  ,3.3841e+003 , -5.8536e+002]

# Sensor 5 settings
SENSOR_5_NAME = 'Sensor 5'
SENSOR_5_CHANNEL = 5
SENSOR_5_COEFFICIENTS = [-2.0675e-009 , 4.6343e-007 , -4.5072e-005 , 2.4926e-003,  -8.6283e-002,  1.9387e+000 , -2.8346e+001 , 2.6227e+002 , -1.4266e+003 , 3.7401e+003 , -8.1280e+002]

# Sensor 6 settings
SENSOR_6_NAME = 'Sensor 6'
SENSOR_6_CHANNEL = 6
SENSOR_6_COEFFICIENTS = [-2.2914e-009 , 5.1419e-007 , -5.0025e-005 , 2.7641e-003 , -9.5444e-002 , 2.1342e+000 , -3.0949e+001 , 2.8262e+002 ,-1.5067e+003 , 3.8349e+003 , -7.3984e+002]

# Sensor 7 settings
SENSOR_7_NAME = 'Sensor 7'
SENSOR_7_CHANNEL = 7
SENSOR_7_COEFFICIENTS = [-2.6392e-009 , 5.8660e-007 , -5.6511e-005 , 3.0913e-003 , -1.0567e-001 , 2.3392e+000 , -3.3595e+001 , 3.0411e+002 ,-1.6109e+003,  4.0998e+003 , -9.6465e+002]

##############################################################
