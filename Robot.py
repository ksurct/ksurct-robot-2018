''' Robot.py

    Describe what components the robot is made of
'''

import asyncio

from Components import *
from Settings import *


class Robot(object):
    ''' Define the components that the robot is made up of '''

    def __init__(self):

        # Set the GPIO numbering mode
        io.setmode(GPIO_MODE)

        output_components = [
            LEDComponent(LED_0_BUTTON, LED_0_PIN),
            ServoComponent(0x40, 0, 'up', 'down', 4096, 0, 10),
            # Motors and servos too
        ]

        # check output components
        for output in output_components:
            assert isinstance(output, OutputComponent)

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

        # check input components
        for input_ in input_components:
            assert isinstance(intput_, InputComponent)
    
    async def produce(self):
        ''' Wait for the sensors to read back a distance '''
        while True:
            await asyncio.sleep(1000)
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
        ''' Stop the Robot's components '''
        
        for output in output_components:
            output.stop()
        
        for input_ in input_components:
            input_.stop()
    
    async def update(self, data_dict):
        ''' Update all the robots components with the data dictionary '''
        tasks = []

        for output in output_components:
            tasks.append(asyncio.ensure_future(output.update(data_dict)))
        
        await asyncio.gather(*tasks)
        
