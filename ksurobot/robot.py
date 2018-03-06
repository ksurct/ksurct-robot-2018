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
        # motor_pca9685 = PCA9685(MOTOR_I2C_ADDRESS)

        # Set pca9685 board frequencies
        servo_pca9685.set_pwm_freq(SERVO_PWM_FREQ)
        # motor_pca9685.set_pwm_freq(MOTOR_PWM_FREQ)

        self.output_components = [
            # Servos
            ServoComponent(servo_pca9685, SERVO_0_CHANNEL, SERVO_0_ON_BUTTON, SERVO_0_OFF_BUTTON,
                            SERVO_0_MAX_PWM, SERVO_0_MIN_PWM, SERVO_0_SPEED),
            ServoComponent(servo_pca9685, SERVO_1_CHANNEL, SERVO_1_ON_BUTTON, SERVO_1_OFF_BUTTON,
                            SERVO_1_MAX_PWM, SERVO_1_MIN_PWM, SERVO_1_SPEED),

            # LED
            LEDComponent(LED_BUTTON, LED_PIN),
        ]

        # check output components
        for output in self.output_components:
            assert isinstance(output, OutputComponent)

        self.input_components = [
            # SensorComponent(SENSOR_0_PIN, SENSOR_0_CHANNEL),
            # SensorComponent(SENSOR_1_PIN, SENSOR_1_CHANNEL),
            # SensorComponent(SENSOR_2_PIN, SENSOR_2_CHANNEL),
            # SensorComponent(SENSOR_3_PIN, SENSOR_3_CHANNEL),
            # SensorComponent(SENSOR_4_PIN, SENSOR_4_CHANNEL),
            # SensorComponent(SENSOR_5_PIN, SENSOR_5_CHANNEL),
            # SensorComponent(SENSOR_6_PIN, SENSOR_6_CHANNEL),
            # SensorComponent(SENSOR_7_PIN, SENSOR_7_CHANNEL),
        ]

        # check input components
        for input_ in self.input_components:
            assert isinstance(intput_, InputComponent)

    async def produce(self):
        ''' Wait for the sensors to read back a distance '''
        await asyncio.sleep(.01)
        return {'dummy_key':'dummy_value'}

        tasks = [asyncio.ensure_future(input_.produce()) for input_ in self.input_components]

        # Wait for all sensors to return data with async
        done, pending = await asyncio.wait(tasks)

        # Package all results into a dictionary
        result = {}

        for task in done:
            print(task.result())

        # return the dictionary
        return result

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

