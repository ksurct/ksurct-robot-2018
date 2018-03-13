import asyncio
import websockets
import pickle
import RPi.GPIO as GPIO
import sys
import socket
import _thread

# Web connectivity imports
import subprocess
import time
import os

from urllib.request import urlopen
from logging import Logger
from contextlib import suppress

import Adafruit_PCA9685  # servo libraries from Adafruit

port = 8055
logger = Logger(__name__)

delay = time.time()
p = 1

# Suppress output from subprocess
DEVNULL = open(os.devnull, 'w')

# Initialize the servos with default I2C address (0x40)
shoulder1 = Adafruit_PCA9685.PCA9685(0x40)
shoulder1.set_pwm_freq(60)				# !! Sets the PWM FOR ALL CHANNELS on 0x40 !!
shoulder1_alt = 380
shoulder2 = Adafruit_PCA9685.PCA9685(0x40)
shoulder2_alt = 150
wrist = Adafruit_PCA9685.PCA9685(0x40)
wrist_alt = 400
fingers = Adafruit_PCA9685.PCA9685(0x40)
elbow = Adafruit_PCA9685.PCA9685(0x40)
elbow_alt = 440
eyes = Adafruit_PCA9685.PCA9685(0x40)
eyes_alt = 300

# Initialize the Drive Motors with I2C address (0x41)
leftMotor = Adafruit_PCA9685.PCA9685(0x41)
leftMotor.set_pwm_freq(1600)				# !!  Sets the PWM FOR ALL channels on 0x41 !!
rightMotor = Adafruit_PCA9685.PCA9685(0x41)

# Servo channel information
SHOULDER1_CHA = 0
SHOULDER2_CHA = 1
EYES_CHA = 5
WRIST_CHA = 3
FINGERS_CHA = 4
ELBOW_CHA = 2
LEFTM_CHA = 14
RIGHTM_CHA = 15

#Initialize servos to the Vision preset
#shoulder2.set_pwm(SHOULDER2_CHA, 0, 480)
#elbow.set_pwm(ELBOW_CHA, 0, 300)
#wrist.set_pwm(WRIST_CHA, 0, 400)
#fingers.set_pwm(FINGERS_CHA, 0, 200)

# Set up the GPIO pin for toggling reverse/forward motors.
GPIO.setmode(GPIO.BCM)
GPIO_FWD_PIN = 19
GPIO_REV_PIN = 26
GPIO.setwarnings(False)
GPIO.setup(GPIO_FWD_PIN, GPIO.OUT)
GPIO.setup(GPIO_REV_PIN, GPIO.OUT)

GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.HIGH);

# The following is a set of definitions for terminal text color
class TextColors:
	WARN = '\033[93m'	# Color used for warnings!
	CONF = '\033[94m'	# Color used for confirmations
	PRINT = '\033[92m'	# Color used to distinguish the standard output of p
	BOLD = '\033[1m'	# Bold text to amplify textclass textColors

class CLserver(object):
    def __init__(self, port):
        self._active_connections = set()
        self.port = port

    async def start_server(self):
        logger.info('server starting up')
        self.server = await websockets.serve(self.handle_new_connection, '0.0.0.0', self.port, timeout=1)

    async def handle_new_connection(self, ws, path):
        global p
        logger.debug('new connection to server')
        self._active_connections.add(ws)
        _thread.start_new_thread(self.test_connection, ())
        while True:
            if p == 2:
                leftMotor.set_all_pwm(0, 0)
                rightMotor.set_all_pwm(0, 0)
            else:
                #print(p)
                result = await ws.recv()
            await self.handle_msg(result)
        self._active_connections.remove(ws)

    async def send(self, msg):  
        logger.debug('sending new message')
        try:
            for ws in self._active_connections:
                asyncio.ensure_future(ws.send(msg))
        except:
            shoulder2.set_all_pwm(0, 0)
            self._active_connections = set()
            asyncio.get_event_loop().close()
           
    def test_connection(self):
        global p
        global delay
        while True:
            if ((time.time() - delay) >= 1):
                p = subprocess.call(['./ip_ping.sh'], shell=True, stdout=DEVNULL, stderr=DEVNULL) 
                if p == 2:
                    print(TextColors.WARN + "!!! IP unconfirmed !!!")	
                    delay = time.time()
                    leftMotor.set_all_pwm(0,0)
                    rightMotor.set_all_pwm(0,0)
                    os._exit(1)
                else:
                    print(TextColors.CONF + " IP Confirmed ")
                    delay = time.time()

#    def set_servos(self, channel, input, servoDelay):
#        global shoulder1, shoulder1_alt
#        if (time.time() - servoDelay) >= 0.009:
#            if channel == 0:
#                shoulder1.set_pwm(channel, 0, shoulder1_alt)
#                shoulder1_alt += 5
#                shoulder1_delay = time.time()

    async def handle_msg(self, msg):
        try:
            logger.debug('new message handled')
            global shoulder1_alt, shoulder2_alt, wrist_alt, elbow_alt, eyes_alt
            msg = pickle.loads(msg)
            if msg != "0":
         #       if msg['lbx']:
         #           print("lbump + x")
                if msg['rbx']:
                    if eyes_alt >= 500:
                        eyes_alt = 500
                    eyes.set_pwm(EYES_CHA, 0, eyes_alt)
                    eyes_alt += 3
                elif msg['x']:  # Left - X
                     if shoulder1_alt <= 235:
                         shoulder1_alt = 235
                     shoulder1.set_pwm(SHOULDER1_CHA, 0, shoulder1_alt) 
                     shoulder1_alt -= 1
               # if msg['lbb']:
               #     print("lbump + b")
                if msg['rbb']:
                    if eyes_alt <= 140:
                        eyes_alt = 140
                    eyes.set_pwm(EYES_CHA, 0, eyes_alt)
                    eyes_alt -= 3
                elif msg['b']:
                    if shoulder1_alt >= 525:
                        shoulder1_alt = 525
                    shoulder1.set_pwm(SHOULDER1_CHA, 0, shoulder1_alt)
                    shoulder1_alt += 1
                if msg['lby']:
                   # print("lbump + y")
                    if wrist_alt >= 530:
                        wrist_alt = 530
                    wrist.set_pwm(WRIST_CHA, 0, wrist_alt)
                    wrist_alt += 1
                elif msg['rby']:
                    if elbow_alt <= 240:
                        elbow_alt = 240
                    elbow.set_pwm(ELBOW_CHA, 0, elbow_alt)
                    elbow_alt -= 1
                elif msg['y']:  # Up - Y
                   # print("Servo up")
                    if shoulder2_alt >= 446: # servo maximum, make sure we do not go over this value
                        shoulder2_alt = 445
                    shoulder2.set_pwm(SHOULDER2_CHA, 0, shoulder2_alt)
                    shoulder2_alt += 1 # CHANGE THIS INCREMENT IF NOT FAST/SLOW ENOUGH
                if msg['lba']:
                   # print("lbump + a")
                    if wrist_alt <= 240:
                        wrist_alt = 240
                    wrist.set_pwm(WRIST_CHA, 0, wrist_alt)
                    wrist_alt -= 1
                elif msg['rba']:
                    if elbow_alt >= 400:
                        elbow_alt = 400
                    elbow.set_pwm(ELBOW_CHA, 0, elbow_alt)
                    elbow_alt += 1
                elif msg['a']:  # Down - A
                   # print("Servo down")
                    if shoulder2_alt <= 150:  # servo minimum, make sure we do not go under this value
                        shoulder2_alt = 150
                    shoulder2.set_pwm(SHOULDER2_CHA, 0, shoulder2_alt)
                    shoulder2_alt -= 1  # CHANGE THIS DECREMENT IF NOT FAST/SLOW ENOUGH
                if msg['vision'] == 1:
                    shoulder1.set_pwm(SHOULDER1_CHA, 0, 380)
                    shoulder1_alt = 380
                    #wrist.set_pwm(WRIST_CHA, 0, 400)
                    #elbow.set_pwm(ELBOW_CHA, 0, 300)
                    #fingers.set_pwm(FINGERS_CHA, 0, 200)
                elif msg['peek'] == 1:
                    eyes.set_pwm(EYES_CHA, 0, 162)
    #                shoulder2.set_pwm(SHOULDER2_CHA, 0, 450)
    #                elbow.set_pwm(ELBOW_CHA, 0, 400)
    #                wrist.set_pwm(WRIST_CHA, 0, 500)
                if msg['neutral']:
                    eyes.set_pwm(EYES_CHA, 0, 250)
                if msg['rstick'] > 0:  # Open the fingers
                    fingers.set_pwm(FINGERS_CHA, 0, 400)
                else:
                    fingers.set_pwm(FINGERS_CHA, 0, 540) #200)
                if msg['rev'] >= 0:
                    # print("Reverse")
                    GPIO.output(GPIO_REV_PIN, GPIO.HIGH)
                    GPIO.output(GPIO_FWD_PIN, GPIO.HIGH)
                    if msg['lstick'] > 0:
                        leftMotor.set_pwm(LEFTM_CHA, 0, msg['rev'])
                        rightMotor.set_pwm(RIGHTM_CHA, 0,  msg['rev'] - (msg['rev']*msg['lstick'] >> 4))
                    elif msg['lstick'] < 0:
                        leftMotor.set_pwm(LEFTM_CHA, 0, msg['rev'] + (msg['rev']*msg['lstick'] >> 4))
                        rightMotor.set_pwm(RIGHTM_CHA, 0, msg['rev'])
                    else:
                        leftMotor.set_pwm(LEFTM_CHA, 0, msg['rev'])
                        rightMotor.set_pwm(RIGHTM_CHA, 0, msg['rev'])
                elif msg['fwd'] >= 0:
                   # print("Forward")
                    GPIO.output(GPIO_FWD_PIN, GPIO.LOW)
                    GPIO.output(GPIO_REV_PIN, GPIO.LOW)
                    if msg['lstick'] < 0:
                        leftMotor.set_pwm(LEFTM_CHA, 0, msg['fwd'] + (msg['fwd']*msg['lstick'] >> 4))
                        rightMotor.set_pwm(RIGHTM_CHA, 0,  msg['fwd'])
                    elif msg['lstick'] > 0:
                       leftMotor.set_pwm(LEFTM_CHA, 0, msg['fwd'])
                       rightMotor.set_pwm(RIGHTM_CHA, 0, msg['fwd'] - (msg['fwd']*msg['lstick'] >> 4))
                    else:
                       leftMotor.set_pwm(LEFTM_CHA, 0, msg['fwd'])
                       rightMotor.set_pwm(RIGHTM_CHA, 0, msg['fwd'])
                else:
                 #   print("Default")
                    GPIO.output(GPIO_FWD_PIN, GPIO.HIGH) # right
                    GPIO.output(GPIO_REV_PIN, GPIO.HIGH) # left
                    if msg['lstick'] < 0:
                        GPIO.output(GPIO_FWD_PIN, GPIO.LOW)
                        leftMotor.set_pwm(LEFTM_CHA, 0, -(4096*msg['lstick']) >> 4)
                        rightMotor.set_pwm(RIGHTM_CHA, 0, -(4096*msg['lstick']) >> 4)
                    elif msg['lstick'] > 0:
                       GPIO.output(GPIO_REV_PIN, GPIO.LOW)
                       leftMotor.set_pwm(LEFTM_CHA, 0, (4096*msg['lstick']) >> 4)
                       rightMotor.set_pwm(RIGHTM_CHA, 0, (4096*msg['lstick']) >> 4)
                    else:
                       # print('default state')
    finally:
                       leftMotor.set_pwm(LEFTM_CHA, 0, 0)
                       rightMotor.set_pwm(RIGHTM_CHA, 0, 0)
                       GPIO.output(GPIO_FWD_PIN, GPIO.LOW)
                       GPIO.output(GPIO_REV_PIN, GPIO.LOW)
                await self.send(pickle.dumps(msg))
        except Exception as e:
            print(e)
            rightMotor.set_all_pwm(0, 0)
            leftMotor.set_all_pwm(0, 0)
            asyncio.get_event_loop().close()

try:
    server = CLserver(port)
    asyncio.get_event_loop().run_until_complete(server.start_server())
    asyncio.get_event_loop().run_forever()
except:
    rightMotor.set_all_pwm(0, 0)
    leftMotor.set_all_pwm(0, 0)
    asyncio.get_event_loop().close()
