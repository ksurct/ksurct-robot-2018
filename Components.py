''' Components.py

    Define components and how they should work for the robot
'''

import asyncio

import RPi.GPIO as io
from Adafruit_PCA9685 import PCA9685

from Settings import MOTOR_PWM_FREQ, SERVO_PWM_FREQ


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

    def __init__(self, pin, channel):
        self.pin = pin
        self.channel = channel
    
    def convert_to_distance(voltage):
        ''' Take the voltage read on the sensor and return the distance '''
        raise NotImplementedError()

    async def produce(self):
        ''' Async funtion to read sensor data on channel from SCI '''
        raise NotImplementedError()
    
    def stop(self):
        ''' Close SCI connection '''
        raise NotImplementedError()


class OutputComponent(Component):

    def update(self, data):
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

    def update(self, data_dict):
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


class PCA9685Mixin(object):
    ''' When a Component class inherites from this this class 
        it gains the ability to communicate over i2c to the 
        PCA9685 board
    '''

    # PWM_FREQ must be set by subclass
    PWM_FREQ = None

    def __init__(self, i2c_address, i2c_channel):
        ''' Creates a PCA9685 object and to send '''
        self.i2c_board = PCA9685(i2c_address)
        self.i2c_board.set_pwm_freq(PWM_FREQ)

        self.i2c_channel = i2c_channel
    
    def set_pwm(self, value):
        ''' Use i2c to set the pwm on self.i2c_channel '''
        self.i2c_board.set_pwm(self.i2c_channel, 0, value)


class MotorComponent(PCA9685Mixin, OutputComponent):

    PWM_FREQ = MOTOR_PWM_FREQ

    def __init__(i2c_address, i2c_channel, feedback_pin, button_axis, reverse=False):
        ''' Setup PCA9685, feedback pin, and button '''

        # Setup PCA9685
        super().__init__(i2c_address, i2c_channel)
        
        # Setup feedback pin
        io.setup(feedback_pin, io.OUT)
        self.feedback_pin

        # Setup button
        self.button_axis = button_axis
        self.reverse = reverse
        
        self.stop()

    def stop(self):
        ''' Stop motor '''
        self.set_pwm(0)

    def update(self, data_dict):
        ''' Update the state of the motor based on the data_dict '''
        self.set_pwm(data_dict[self.button_axis])
    

class ServoComponent(OutputComponent):

    PWM_FREQ = SERVO_PWM_FREQ

    def __init__(self, i2c_address, i2c_channel, on_button, off_button, max_pwm, min_pwm, button_speed):
        ''' Setup PCA9685 and button logic '''

        # Setup PCA9685
        super().__init__(i2c_address, i2c_channel)

        # Setup button
        self.on_button = on_button
        self.off_button = off_button
        
        self.max_pwm = max_pwm
        self.min_pwm = min_pwm

        # self.current = min_pwm
        self.target = min_pwm
        # self.servo_speed = servo_speed
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
            if self.target + self.button_speed < self.max_pwm:
                self.target += self.button_speed
            else:
                self.target = self.max_pwm
        
        if data_dict[self.off_button]:
            if self.target - self.button_speed > self.min_pwm:
                self.target -+ self.button_speed
            else:
                self.target = self.min_pwm
        
        self.set_pwm(self.target)


