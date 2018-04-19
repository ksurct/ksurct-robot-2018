''' components.py

    Define components and how they should work for the robot
'''

import asyncio
import logging
import RPi.GPIO as io
import time
import threading

from hardware import MAX192AEPP

logger = logging.getLogger("__main__")


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
            the distance (in centimeters) based on the coefficients and voltage. 
        '''
        index = 0
        distance = 0
        while index < len(self.coefficients):
            distance += self.coefficients[index]*(voltage**(len(self.coefficients)-index-1)) # The -1 here is to fix off by 1 error. Coeff[10] should be a constant term.
            index += 1
        return distance

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

    def __init__(self, pca9685=None, pca9685_channel=None, button=None, value=None):
        ''' Setup a button to control a pin to control an LED

            - pca9685: an object to output the pwm
            - pca9685_channel: the channel to output to using the pca9685
            - button: the controller button that will toggle the LED
            - value: the output value, larger is brighter
        '''

        self.pca9685 = pca9685
        self.pca9685_channel = pca9685_channel
        self.button = button
        self.value = value
        self._state = 0

        self.stop()

    def stop(self):
        ''' Turn off all pins '''
        self.output(False)
    
    def output(self, value):
        ''' Output to the LED's through i2c '''
        if value:
            self.pca9685.set_pwm(self.pca9685_channel, 0, self.value)
        else:
            self.pca9685.set_pwm(self.pca9685_channel, 0, 0)

    async def update(self, data_dict):
        ''' Update the state of the LED '''
        if self._state == 0:
            if data_dict[self.button]:
                self.output(True)
                self._state = 3
        elif self._state == 1:
            if not data_dict[self.button]:
                self._state = 0
        elif self._state == 2:
            if data_dict[self.button]:
                self.output(False)
                self._state = 1
        elif self._state == 3:
            if not data_dict[self.button]:
                self._state = 2


class MotorComponent(Component):

    def __init__(self, pca9685=None, pca9685_channel=None, dir_pin=None, reverse=False):
        ''' Setup PCA9685, and other settings
        
            - pca9685: an object to output the pwm
            - pca9685_channel: the channel to output to using the pca9685
            - min_pwm: the minimum value that we can output to the motor
            - dir_pin: the GPIO pin that will output the direction to the motor controller
            - feedback_pin: (NOT USED) the pin that provides feedback about the motors speed
            - reverse: reverses the direction output if true
        '''

        # Setup PCA9685
        self.pca9685 = pca9685
        self.pca9685_channel = pca9685_channel

        # Setup the pin to output the direction of the motors
        self.dir_pin = dir_pin
        io.setup(self.dir_pin, io.OUT)

        self.min_pwm = 0

        # Reverses the output when true
        self.reverse = reverse

        self.stop()

    def stop(self):
        ''' Stop motor '''
        self.pca9685.set_pwm(self.pca9685_channel, 0, 0)
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
            self.pca9685.set_pwm(self.pca9685_channel, 0, value)

        logging.getLogger('__main__').info('Setting: {}, {}'.format(self.pca9685_channel, value))

        # if not value: # Just to save time
        io.output(self.dir_pin, direction ^ self.reverse)


class MotorController(OutputComponent):

    def __init__(self, fwd_axis=None, back_axis=None, steer_axis=None, steer_speed=0, motors=None, min_pwm=0, reverse=False):
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
        self.min_pwm = min_pwm
        for motor in self.motors:
            motor.min_pwm = self.min_pwm

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
        amt = (abs(steer)*self.steer_speed)
        if steer < 0:
            r_val = val - amt // 2
            l_val = val + amt // 2
        else:
            r_val = val + amt // 2
            l_val = val - amt // 2

        # Map values to a range between min_pwm and 4095
        # but keep at 0 if already at zero
        slope = self.min_pwm / 4095

        r_val = min(r_val, 4095)
        l_val = min(l_val, 4095)
        r_val = max(r_val, -4096)
        l_val = max(l_val, -4096)
        
        if r_val > 0: r_val = int(slope * r_val) + self.min_pwm
        if r_val < 0: r_val = int(slope * r_val) - self.min_pwm
        
        if l_val > 0: l_val = int(slope * l_val) + self.min_pwm
        if l_val < 0: l_val = int(slope * l_val) - self.min_pwm

        # logging.getLogger('__main__').info('Controller values: {0}, {1}'.format(r_val, l_val))


        self.motors[0].output(r_val) # Front Right
        self.motors[1].output(l_val) # Front Left
        self.motors[2].output(r_val) # Back Right
        self.motors[3].output(l_val) # Back Left


class ServoComponent(OutputComponent):

    UP_BUTTON = 'up'
    DOWN_BUTTON = 'down'
    AXIS = 'r_stick_y'

    def __init__(self, pca9685=None, pca9685_channel=None, modifier=None, max_pwm=None, min_pwm=None,
                    presets=None, control_speed=None, servo_speed=None, reverse=False):
        ''' Setup PCA9685 and button logic

            - pca9685: an object to output the pwm
            - pca9685_channel: the channel to output to using the pca9685
            - modifier: the button that will control the fine-tuning movements
            - max_pwm: the maximum value that we can output to the servo
            - min_pwm: the minimum value that we can output to the servo
            - presets: A list that consits of tuples in the form (button_name, preset_value)
                    with the highest priorty at the front
            - control_speed: the speed that the user is controling the servo with
            - servo_speed: the speed that the servo moves at
         '''

        # Setup PCA9685 connection
        self.pca9685 = pca9685

        self.pca9685_channel = int(pca9685_channel)

        self.modifier = modifier

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

        self.control_speed = control_speed
        self.servo_speed = servo_speed

        self.active = True
        self.setup()

    def stop(self):
        ''' Stop Servo '''
        self.active = False

    def setup(self):
        ''' Move the servo until it reaches it's starting position '''
        t = threading.Thread(target=self.loop)
        t.start()

    def output(self):
        self.pca9685.set_pwm(self.channel, 0, self.target)

    async def update(self, data_dict):
        ''' Update the target of the servo based on the data_dict '''
        
        # Validate that data is in the set range
        if self.target > self.max_pwm or self.target < self.min_pwm:
            logger.warn('Target servo pwm out of range')
            self.stop()
            return

        # Get Modifier
        mod = data_dict[self.modifier]

        if mod:
            if data_dict[self.UP_BUTTON]:
                self.target += self.control_speed
            if data_dict[self.DOWN_BUTTON]:
                self.target -= self.control_speed
            
            self.target += data_dict[self.AXIS] * self.control_speed

        # Set to a preset value and override manual control
        for preset in self.presets:
            if data_dict[preset[0]]:
                self.target = int(preset[1])
                break

    def loop(self):
        ''' Main loop of special thread '''
        while self.active:
            self.move_towards()
            time.sleep(0.1)

    def move_towards(self):
        ''' Move the servo to self.target,
            increment self.current according to the servo speed and time elapsed,
            then move to new current and save the state
        '''
        # Calculate the amount to move by
        time_delta = time.time() - self._last_time
        move_amt = int(self.servo_speed * time_delta)
        if move_amt < 1:
            return

        # Increment towards the target value in the right direction without being out of bounds
        if self.current < self.target:
            self.current = min(self.current + move_amt, self.target, self.max_pwm)
        elif self.current >= self.target:
            self.current = max(self.current - move_amt, self.target, self.min_pwm)

        # Output
        self.pca9685.set_pwm(self.pca9685_channel, 0, self.current) # Move the servo CHECK OUT THE 0

        # Save state for future
        self._last_time = time.time()
        self._last_ouput = self.current
