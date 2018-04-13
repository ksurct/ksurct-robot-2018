''' components.py

    Define components and how they should work for the robot
'''

import asyncio
import logging
import RPi.GPIO as io

from hardware import MAX192AEPP

import time

logger = logging.getLogger("__main__")

class Component(object):

    def __init__(self):
        raise NotImplementedError()

    def stop(self):
        ''' Stop the component '''
        raise NotImplementedError()


class InputComponent(Component):

    async def produce(self):
        ''' Return the data for read from this element '''
        raise NotImplementedError()


class SensorComponent(InputComponent):
    ''' Input Component that reads a voltage from a adc
        and then converts that to a distance
    '''

    def __init__(self, name, channel, coefficients):
        ''' Setup channel and coefficients '''
        self.name = name
        self.channel = channel
        self.coefficients = coefficients

    def _convert_to_distance(self, voltage):
        ''' Take the voltage read on the sensor and return
            the distance based on the coefficients '''
        # Not complete
        return voltage

    def _get_value(self):
        ''' Get the raw value from the adc about the sensor '''
        return MAX192AEPP.read_channel(self.channel)

    async def produce(self):
        ''' Async funtion to read sensor data on channel from SCI '''
        return self.name, self._convert_to_distance(self._get_value())

    def stop(self):
        ''' Close SCI connection '''
        pass


class OutputComponent(Component):

    async def update(self, data):
        raise NotImplementedError()


class LEDComponent(OutputComponent):

    def __init__(self, button, pin):
        ''' Setup a button to control a pin to control an LED '''

        self.button = button
        self.pin = pin
        self._state = 0

        # Setup output pins
        io.setup(self.pin, io.OUT)
        self.stop()

    def stop(self):
        ''' Turn off all pins '''
        io.output(self.pin, False)

    async def update(self, data_dict):
        ''' Update the state of the LED '''
        if self._state == 0:
            if data_dict[self.button]:
                io.output(self.pin, True)
                self._state = 3
        elif self._state == 1:
            if not data_dict[self.button]:
                # io.output(self.pin, False) # redundant
                self._state = 0
        elif self._state == 2:
            if data_dict[self.button]:
                io.output(self.pin, False)
                self._state = 1
        elif self._state == 3:
            if not data_dict[self.button]:
                # io.output(self.pin, True) # redundant
                self._state = 2


class MotorComponent(OutputComponent):

    def __init__(pca9685, pca9685_channel, feedback_pin, button_axis, reverse=False):
        ''' Setup PCA9685, feedback pin, and button '''

        # Setup PCA9685
        self.pca9685 = pca9685
        self.pca9685_channel = pca9685_channel

        # Setup feedback pin
        io.setup(feedback_pin, io.IN)
        self.feedback_pin

        # Setup button
        self.button_axis = button_axis
        self.reverse = reverse

        self.stop()

    def stop(self):
        ''' Stop motor '''
        self.pca9685.set_pwm(self.pca9685_channel, 0, 0)

    async def update(self, data_dict):
        ''' Update the state of the motor based on the data_dict '''
        self.pca9685.set_pwm(self.pca9685_channel, 0, data_dict[self.button_axis])


class ServoComponent(OutputComponent):

    def __init__(self, pca9685, pca9685_channel, manual_axis, max_pwm, min_pwm, presets, servo_speed):
        ''' Setup PCA9685 and button logic

            - pca9685: an object to output the pwm
            - pca9685_channel: the channel to output to using the pca9685
            - manual_axis: the axis that will control the fine-tuning movements
            - max_pwm: the maximum value that we can output to the servo
            - min_pwm: the minimum value that we can output to the servo
            - presets: A list that consits of tuples in the form (button_name, preset_value)
                    with the highest priorty at the front
            - servo_speed: the speed that the servo moves at
         '''

        # Setup PCA9685 connection
        self.pca9685 = pca9685
        self.pca9685_channel = int(pca9685_channel)

        self.manual_axis = manual_axis

        self.max_pwm = int(max_pwm)
        self.min_pwm = int(min_pwm)

        # Check presets for errors
        for p in presets:
            if p[1] > self.max_pwm or p[1] < self.min_pwm:
                logger.warn("A preset value is out of range!!!!")
        self.presets = presets

        self.current = 0
        self.target = self.min_pwm
        self._last_time = time.time()
        self._last_ouput = self.current
        
        self.servo_speed = servo_speed

        self.setup()

    def stop(self):
        ''' Stop Servo '''
        self.target = self.current

    def setup(self):
        ''' Move the servo until it reaches it's starting position '''
        while self.current != self.target:
            self.move_towards()
            asyncio.sleep(0.01)

    async def update(self, data_dict):
        ''' Update the target of the servo based on the data_dict '''

        # Validate that data is in the set range
        if self.target > self.max_pwm or self.target < self.min_pwm:
            logger.warn('Target servo pwm out of range')
            self.stop()
            return

        # Check data_dict for manual control
        if data_dict[self.manual_axis] > 0:
            self.target = self.target + self.servo_speed
        elif data_dict[self.manual_axis] < 0:
            self.target = self.target - self.servo_speed

        # Set to a preset value and override manual control
        for preset in self.presets:
            if data_dict[preset[0]]:
                self.target = int(preset[1])
                break

        # Slowely move to where we want to be
        if self.current != self.target:
            self.move_towards()

    
    def move_towards(self):
        ''' Move the servo to self.target,
            increment self.current according to the servo speed and time elapsed,
            then move to new current and save the state
        '''
        # Calculate the amount to move by
        time_delta = time.time() - self._last_time
        move_amt = int(self.servo_speed * time_delta)
        if move_amt < 1: move_amt = 1

        # Increment towards the target value in the right direction without being out of bounds
        if self.current < self.target:
            self.current = min(self.current + move_amt, self.target, self.max_pwm)
        elif self.current >= self.target:
            self.current = max(self.current - move_amt, self.target, self.min_pwm)
        
        # Output if change is needed
        if self.current != self._last_ouput:
            self.pca9685.set_pwm(self.pca9685_channel, 0, self.current) # Move the servo CHECK OUT THE 0
        
        # Save state for future
        self._last_time = time.time()
        self._last_ouput = self.current
