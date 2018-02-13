''' Robot.py

    Describe what components the robot is made of
'''

from Components import *
from Settings import *


class Robot(object):
    '''
        Define the components that the robot is made up of
    '''

    def __init__(self):

        # Setup drive motors
        self.drive_motor_0 = DCMotorComponent(
            DRIVE_MOTOR_0_P1,
            DRIVE_MOTOR_0_P2,
            DRIVE_MOTOR_0_HIGH,
            DRIVE_MOTOR_0_LOW,
            reverse=DRIVE_MOTOR_0_REVERSE
        )

        self.drive_motor_1 = DCMotorComponent
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
    
    async def produce(self):
        '''
            Wait for the sensors to read back a distance
        '''
        sensor_0_task = asyncio.ensure_future(self.sensor_0.produce())
        sensor_1_task = asyncio.ensure_future(self.sensor_1.produce())
        sensor_2_task = asyncio.ensure_future(self.sensor_2.produce())
        sensor_3_task = asyncio.ensure_future(self.sensor_3.produce())

        # Wait for all sensors to return data with async
        done, pending = await asyncio.wait(
            [sensor_0_task, sensor_1_task, sensor_2_task, sensor_3_task],
            return_when=asyncio.ALL_COMPLETED,
        )

        # Package all results into a dictionary
        result = {}
        
        result[self.sensor_0.channel] = sensor_0_task.result()
        result[self.sensor_1.channel] = sensor_1_task.result()
        result[self.sensor_2.channel] = sensor_2_task.result()
        result[self.sensor_3.channel] = sensor_3_task.result()
        
        # return the dictionary
        return result
    
    def stop(self):
        '''
            Stop the Robot
        '''
        raise NotImplementedError()
    
    async def update(self, data):
        '''
            Update all the robots components with the data dictionary
        '''
        raise NotImplementedError()
