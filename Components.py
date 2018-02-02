''' Components.py

    Define components and how they should work for the bot
'''

from RPi.GPIO as io


class Component(object):

    def __init__(self):
        raise NotImplementedError()
    
    def stop(self):
        raise NotImplementedError()

    def update(self, data):
        raise NotImplementedError()


class LEDComponent(Component):

    def __init__(self, button, pin):

        self.button = button
        self.pin = pin
        self._state = 0

        # Setup output pins
        io.setup(self.pin, io.OUT)
        self.stop()
    
    def stop(self):
        # Turn off all pins
        io.output(self.pin, False)

    def update(self, data):
        # Update the state of the LED
        if self._state == 0:
            if data[self.button]:
                io.output(self.pin, True)
                self._state = 3
        elif self._state == 1:
            if !data[self.button]:
                io.output(self.pin, False)
                self._state = 0
        elif self._state == 2:
            if data[self.button]:
                io.output(self.pin, False)
                self._state = 1
        elif self._state == 3:
            if !data[self.button]:
                io.output(self.pin, True)
                self._state = 2
        

class SensorComponent(Component):

    def __init__(self, pin, channel):
        self.pin = pin
        self.channel = channel
    
    async def produce(self):
        pass


class MotorComponent(Component):

    def __init__(self, p1, p2, reverse=False):
        
        self.p1 = p1
        self.p2 = p2
        self.reverse = reverse
        
        # Setup output pins
        io.setup(p1, io.OUT)
        io.setup(p2, io.OUT)
        self.stop()

    def stop(self):
        # Turn off all pins
        io.output(p1, False)
        io.output(p2, False)

    def update(self, data):
        pass


class DCMotorComponent(MotorComponent):

    def __init__(self, p1, p2, high_button, low_button, reverse=False):

        super().__init__(sefl, p1, p2, reverse=reverse)
        self.high_button = high_button
        self.low_button = low_button
    
    def update(self, data):
        # Update output pins
        io.output(p1, data[self.high_button] ^ self.reverse)
        io.output(p2, data[self.low_button] ^ self.reverse)


class PWMMotorComponent(MotorComponent):

    def __init__(self, p1, p2, pwm_pin, axis_button, reverse=False):

        super().__init__(self, p1, p2, reverse=reverse)
        
        self.axis_button = axis_button

        # Setup pwm pin
        self.pwm_pin = pwm_pin
        io.setup(pwm_pin, io.OUT)
    
    def update(self, data):
        pass
    
    
