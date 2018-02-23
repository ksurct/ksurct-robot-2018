''' Robot.py

    Describe what components the robot is made of
'''

import asyncio

from Components import *
from Settings import *


class Robot(object):
    ''' Define the components that the robot is made up of '''

    def __init__(self):

        output_components = [
            LEDComponent(LED_0_BUTTON, LED_0_PIN),
            LEDComponent(LED_1_BUTTON, LED_1_PIN),
            # Motors and servos too
        ]

        input_components = [
            SensorComponent(SENSOR_0_PIN, SENSOR_0_CHANNEL),
            SensorComponent(SENSOR_1_PIN, SENSOR_1_CHANNEL),
            SensorComponent(SENSOR_2_PIN, SENSOR_2_CHANNEL),
            SensorComponent(SENSOR_3_PIN, SENSOR_3_CHANNEL),
            SensorComponent(SENSOR_4_PIN, SENSOR_4_CHANNEL),
            SensorComponent(SENSOR_5_PIN, SENSOR_5_CHANNEL),
            SensorComponent(SENSOR_6_PIN, SENSOR_6_CHANNEL),
            SensorComponent(SENSOR_7_PIN, SENSOR_7_CHANNEL),
        ]
    
    async def produce(self):
        ''' Wait for the sensors to read back a distance '''

        await asyncio.sleep(.01)
        return {"hello": 1}

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
        ''' Stop the Robot '''
        for output in output_components:
            assert isinstance(output, Component)
            output.stop()
        
        for input_ in input_components:
            assert isinstance(intput_, Component)
            input_.stop()
    
    async def update(self, data):
        ''' Update all the robots components with the data dictionary '''
        
        await asyncio.sleep(0.01)
