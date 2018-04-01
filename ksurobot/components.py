''' components.py

    Define components and how they should work for the robot
'''

import asyncio
import logging
import RPi.GPIO as io

from hardware import MAX192AEPP

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

    def __init__(self, pca9685, pca9685_channel, on_button, off_button, max_pwm, min_pwm, button_speed):
        ''' Setup PCA9685 and button logic '''

        # Setup PCA9685
        self.pca9685 = pca9685
        self.pca9685_channel = pca9685_channel

        # Setup button
        self.on_button = on_button
        self.off_button = off_button

        self.max_pwm = max_pwm
        self.min_pwm = min_pwm

        self.current = min_pwm
        self.target = min_pwm
        # self.servo_speed = servo_speed logging.getLogger 
        self.button_speed = button_speed

    def stop(self):
        ''' Stop Servo '''
        pass
        # self.target = self.current

    # async def async_loop(self):
    #     ''' Loop to be ran in async loop '''
    #     while True:
    #         if self.current < self.target:
    #             if self.current + self.servo_speed < self.target:
    #                 self.current += self.servo_speed
    #                 self.set_pwm(self.current)
    #             else:
    #                 self.current = self.target

    #         asyncio.sleep(0)


    async def update(self, data_dict):
        ''' Update the target of the servo based on the data_dict '''

        if data_dict[self.on_button]:
            self.target = min(self.target + self.button_speed, self.max_pwm)

        elif data_dict[self.off_button]:
            self.target = max(self.target - self.button_speed, self.min_pwm)

        #self.pca9685.set_pwm(self.pca9685_channel, 0, self.target)
        #slowely move to where we want to be
        while self.current != self.target:
            self.move_to()

    
    def move_to(self):
        '''move the servo to self.target, call this function in a loop'''
        '''increment self.current according to the step size, then move to new current'''
        #PWM_STEP_SIZE = 1; #the step size, a higher number means moving faster
        #this has been added to settings.py, uncomment for testing probably

        goodDataFlag = (self.target <= self.max_pwm) && (self.target >= self.min_pwm) #if data is in valid range

        if(goodDataFlag): #if you have good data
            if self.current <= self.target:
                self.current += PWM_STEP_SIZE #increment up by that size
                if self.current > self.target: #if you've gone too far, set to target
                    self.current = self.target
            elif self.current >= self.target: 
                self.current -+ PWM_STEP_SIZE
                if self.current < self.target: #if you've gone too far, set to target
                    self.current = self.target
            self.pca9685.set_pwm(self.pca9685_channel, 0, self.current) #move the servo CHECK OUT THE 0
        else:
            logger.warn("Bad target for servo")
           


