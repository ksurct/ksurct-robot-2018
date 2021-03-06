''' robot.py

    Describe what components the robot is made of
'''

import asyncio

from Adafruit_PCA9685 import PCA9685

from components import *
from settings import *


class Robot(object):
    ''' Define the components that the robot is made up of '''

    def __init__(self):

        # Set the GPIO numbering mode
        io.setmode(GPIO_MODE)

        # Connect to servo and motor pca9685 boards
        servo_pca9685 = PCA9685(SERVO_I2C_ADDRESS)
        motor_pca9685 = PCA9685(MOTOR_I2C_ADDRESS)

        # Set pca9685 board frequencies
        servo_pca9685.set_pwm_freq(SERVO_PWM_FREQ)
        motor_pca9685.set_pwm_freq(MOTOR_PWM_FREQ)

        motors = [
            # Motors
            MotorComponent(pca9685=motor_pca9685, pca9685_channel=0, dir_pin=33), # Front Right
            MotorComponent(pca9685=motor_pca9685, pca9685_channel=1, dir_pin=29, reverse=True), # Front Left
            MotorComponent(pca9685=motor_pca9685, pca9685_channel=2, dir_pin=35), # Back Right
            MotorComponent(pca9685=motor_pca9685, pca9685_channel=3, dir_pin=31, reverse=True), # Back Left
        ]

        self.output_components = [
            # Servos
            ServoComponent(pca9685=servo_pca9685, pca9685_channel=SERVO_0_CHANNEL, modifier=SERVO_0_MODIFIER, max_pwm=SERVO_0_MAX_PWM,
                            min_pwm=SERVO_0_MIN_PWM, presets=SERVO_0_PRESETS, control_speed=SERVO_0_CONTROL_SPEED, servo_speed=SERVO_0_SPEED, 
                            reverse=False),
            ServoComponent(pca9685=servo_pca9685, pca9685_channel=SERVO_1_CHANNEL, modifier=SERVO_1_MODIFIER, max_pwm=SERVO_1_MAX_PWM,
                            min_pwm=SERVO_1_MIN_PWM, presets=SERVO_1_PRESETS, control_speed=SERVO_1_CONTROL_SPEED, servo_speed=SERVO_1_SPEED, 
                            reverse=False),
            ServoComponent(pca9685=servo_pca9685, pca9685_channel=SERVO_2_CHANNEL, modifier=SERVO_2_MODIFIER, max_pwm=SERVO_2_MAX_PWM,
                            min_pwm=SERVO_2_MIN_PWM, presets=SERVO_2_PRESETS, control_speed=SERVO_2_CONTROL_SPEED, servo_speed=SERVO_2_SPEED, 
                            reverse=False),

            # Motors
            MotorController(fwd_axis=MOTOR_FORWARD_AXIS, back_axis=MOTOR_BACKWARD_AXIS, steer_axis=MOTOR_STEER_AXIS,
                                    steer_speed=MOTOR_STEER_SPEED, motors=motors, min_pwm=MOTOR_MIN_PWM, reverse=True),

            # LED
            LEDComponent(pca9685=servo_pca9685, pca9685_channel=LED_CHANNEL, button=LED_BUTTON, value=LED_VALUE),
        ]

        # check output components
        for output in self.output_components:
            assert isinstance(output, OutputComponent)

        # Commented out sensors for debug, we removed the actual sensors / pcb from the bot
        
        self.input_components = [
        #   SensorComponent(SENSOR_0_NAME, SENSOR_0_CHANNEL, SENSOR_0_COEFFICIENTS),
        #   SensorComponent(SENSOR_1_NAME, SENSOR_1_CHANNEL, SENSOR_1_COEFFICIENTS),
        #   SensorComponent(SENSOR_2_NAME, SENSOR_2_CHANNEL, SENSOR_2_COEFFICIENTS),
        #   SensorComponent(SENSOR_3_NAME, SENSOR_3_CHANNEL, SENSOR_3_COEFFICIENTS),
        #   SensorComponent(SENSOR_4_NAME, SENSOR_4_CHANNEL, SENSOR_4_COEFFICIENTS),
        #   SensorComponent(SENSOR_5_NAME, SENSOR_5_CHANNEL, SENSOR_5_COEFFICIENTS),
        #   SensorComponent(SENSOR_6_NAME, SENSOR_6_CHANNEL, SENSOR_6_COEFFICIENTS),
        #   SensorComponent(SENSOR_7_NAME, SENSOR_7_CHANNEL, SENSOR_7_COEFFICIENTS),
        ]
        

        # check input components
        for input_ in self.input_components:
            assert isinstance(input_, InputComponent)

    async def produce(self):
        ''' Wait for the sensors to read back a distance '''

        tasks = [asyncio.ensure_future(input_.produce()) for input_ in self.input_components]

        # Wait for all sensors to return data with async
        done, pending = await asyncio.wait(tasks)

        # Package all results into a dictionary
        data_dict = {}

        for task in done:
            key, value = task.result()
            data_dict[key] = value

        # return the dictionary
        return data_dict

    def stop(self):
        ''' Stop the Robot's components '''

        for output in self.output_components:
            output.stop()

        for input_ in self.input_components:
            input_.stop()

    async def update(self, data_dict):
        ''' Update all the robots components with the data dictionary '''
        tasks = []

        for output in self.output_components:
            tasks.append(asyncio.ensure_future(output.update(data_dict)))

        await asyncio.gather(*tasks)

