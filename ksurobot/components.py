''' components.py

    Define components and how they should work for the robot
'''

import asyncio

import RPi.GPIO as io

from hardware import MAX192AEPP

import logging


class Component(object):

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

    async def update(self, data_dict):
        raise NotImplementedError()


class LEDComponent(OutputComponent):

    def __init__(self, button, pin):
        ''' Setup a button to control a pin to control an LED
        
            - button: the controller button that will toggle the LED
            - pin: the GPIO pin that the LED in controlled from
        '''

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


class MotorComponent(Component):

    def __init__(self, pca9685=None, channel=None, min_pwm=0, dir_pin=None, feedback_pin=None, reverse=False, kp = 0, ki = 0, kd = 0):
        ''' Setup PCA9685, and other settings
        
            - pca9685: an object to output the pwm
            - channel: the channel to output to using the pca9685
            - min_pwm: the minimum value that we can output to the motor
            - dir_pin: the GPIO pin that will output the direction to the motor controller
            - feedback_pin: (NOT USED) the pin that provides feedback about the motors speed
            - reverse: reverses the direction output if true
        '''

        # Setup PCA9685
        self.pca9685 = pca9685
        self.channel = channel

        # Setup the pin to output the direction of the motors
        self.dir_pin = dir_pin
        io.setup(self.dir_pin, io.OUT)

        self.min_pwm = min_pwm

        # Setup feedback pin
        self.feedback_pin = feedback_pin
        # io.setup(self.feedback_pin, io.IN)

        # Reverses the output when true
        self.reverse = reverse

        # Constants for PID loop
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # Last time for PID loop
        (float)self._last_time = time.time()
        (float)self._prev_err = 0

        self.stop()

    def stop(self):
        ''' Stop motor '''
        self.pca9685.set_pwm(self.channel, 0, 0)
        self.last_value = 0

    def output(self, value):
        ''' Update the state of the motor based on the value given
            Value should be a number be a number that is [-4096, 4095]
        '''

        if self.last_value == 0:
            if abs(value) <= self.min_pwm:
                return # Don't output again if the value stays at zero
        else:
            if abs(value) <= self.min_pwm:
                value = 0

        if self.last_value == value:
            return # Don't output if the value hasn't changed
        self.last_value = value

        direction = 0
        if value < 0:
            direction = 1
            value = abs(value)
        if value < 4096:
            self.pca9685.set_pwm(self.channel, 0, value + pid_calculate(self)) 

        logging.getLogger('__main__').info('Setting: {}, {}'.(self.channel, value))

        # if not value: # Just to save time
        io.output(self.dir_pin, direction ^ self.reverse)

    def pid_calculate(self):
        ''' calculates the error term
        '''
        (float)time_delta = time.time() - self._last_time
        (float)current_speed = pid_calc_speed(self, time_delta)
        (float)err = desired_speed - current_speed # this is our error term
        '''need desired speed, get rough estimates of max and min speed for desired speed, have it scale linearlly with analog input'''

        # Integral term
        (float)integral += err * time_delta # old school integral
        # MAY NEED A LIMIT, SO IT DOESNT FREAK OUT

        # Derivative term
        (float)derivative = (err - self._prev_err) / time_delta # change in error over change in time

        delta_output_speed = self.kp * err + self.ki * integral + self.kd * derivative
        # left_motor_speed = desired_speed + delta
        # delta_ouput_speed is change in output_speed
        # sum the two and output it

        self._prev_err = err
        self._last_time = time.time()

        #set limit on output to valid pwm 
        return delta_output_speed


    def pid_calc_speed(self):
        ''' calculates the current speed using interrupt data 
        '''
        current_speed = ((MOTOR_TICKS_PER_ROTATE) * NUM_TICKS) / time_delta
        #clear ticks
        raise NotImplementedError
        return current_speed
        '''
        current speed in (m/s) = ((m/ticks) * ticks) / time
        finish this when I know how we get ticks
        '''




class MotorController(OutputComponent):

    def __init__(self, fwd_axis=None, back_axis=None, steer_axis=None, steer_speed=100, motors=None, reverse=False):
        ''' Setup controls and individual motors

            - fwd_axis: a button axis with a range of -4096 to 4095
            - back_axis: a button axis with a range of -4096 to 4095
            - steer_axis: a button axis with a range of -10 to 10
            - steer_speed: the speed multipler for steering
            - motors: a list of motor components, in order: FR, BR, BL, FL
            - reverse: reverses the direction output if true
        '''
        self.fwd_axis = fwd_axis
        self.back_axis = back_axis
        self.steer_axis = steer_axis

        self.steer_speed = steer_speed
        self.reverse = reverse

        self.motors = motors

        self.stop()
    
    def stop(self):
        ''' Stop the motors '''
        for motor in self.motors:
            motor.stop()
    
    async def update(self, data_dict):
        ''' Update the state of the 4 motors '''

        fwd, back = (data_dict[self.fwd_axis] + 4096) // 2, (data_dict[self.back_axis] + 4096) // 2
        steer = -data_dict[self.steer_axis] if self.reverse else data_dict[self.steer_axis]

        val = fwd - back
        if steer < 0:
            r_val = val - (abs(steer)*self.steer_speed)
            l_val = val
        else:
            r_val = val
            l_val = val - (abs(steer)*self.steer_speed)

        logging.getLogger('__main__').info('Controller values: {0}, {1}'.format(r_val, l_val))

        self.motors[0].output(r_val) # Front Right
        self.motors[1].output(r_val) # Back Right
        self.motors[2].output(l_val) # Back Left
        self.motors[3].output(l_val) # Front Left


class ServoComponent(OutputComponent):

    def __init__(self, pca9685, channel, up_button, down_button, max_pwm, min_pwm, button_speed):
        ''' Setup PCA9685 and button logic '''

        # Setup PCA9685
        self.pca9685 = pca9685
        self.channel = channel

        # Setup button
        self.up_button = up_button
        self.down_button = down_button

        # Set limits
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

    def output(self):
        self.pca9685.set_pwm(self.channel, 0, self.target)

    async def update(self, data_dict):
        ''' Update the target of the servo based on the data_dict '''

        if data_dict[self.up_button]:
            self.target = min(self.target + self.button_speed, self.max_pwm)

        elif data_dict[self.down_button]:
            self.target = max(self.target - self.button_speed, self.min_pwm)

        self.output()

