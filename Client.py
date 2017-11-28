'''
Client.py
'''
import websockets
import asyncio
from contextlib import suppress
from xbox import Controller
import pickle
import sys

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

Controller.init()
controller = Controller(0)
oldRobot = {}


async def SendMessage():
    '''
        Send the state of the controller to the server
    '''
    
    logging.debug('pre IP connect')
    websocket = await websockets.connect('ws://10.132.13.137:8055')
    logging.info('Sent message')
    try:
        while True:
            controller.update()
            
            robot = {}

            # General buttons
            robot['x'] = 1 if controller.x() else 0
            robot['y'] = 1 if controller.y() else 0
            robot['a'] = 1 if controller.a() else 0
            robot['b'] = 1 if controller.b() else 0
            
            # Triggers
            robot['r_trigger'] = int(controller.right_trigger() >> 3)
            robot['l_trigger'] = int(controller.left_trigger() >> 3)

            # Analog sticks
            r_stick_x = round(controller.right_x(), 1)
            r_stick_y = round(controller.right_y(), 1)
            l_stick_x = round(controller.left_x(), 1)
            l_stick_y = round(controller.left_y(), 1)
            robot['r_stick'] = (int(10*r_stick_x) if abs(r_stick_x) > 0.1 else 0,
                                int(-10*r_stick_y) if abs(r_stick_y) > 0.1 else 0 )
            robot['l_stick'] = (int(10*l_stick_x) if abs(l_stick_x) > 0.1 else 0,
                                int(-10*l_stick_y) if abs(l_stick_y) > 0.1 else 0 )
            
            # Bumpers
            robot['r_bump'] = 1 if controller.right_bumper() else 0
            robot['l_bump'] = 1 if controller.left_bumper() else 0
            
            # D-pad
            robot['left'] = 1 if str(controller.hat).strip() == 'l' else 0
            robot['right'] = 1 if str(controller.hat).strip() == 'r' else 0
            robot['up'] = 1 if str(controller.hat).strip() == 'u' else 0
            robot['down'] = 1 if str(controller.hat).strip() == 'd' else 0

            # # Left bumper combinations
            # robot['lbx'] = 1 if controller.left_bumper() and controller.x() else 0
            # robot['lby'] = 1 if controller.left_bumper() and controller.y() else 0
            # robot['lbb'] = 1 if controller.left_bumper() and controller.b() else 0
            # robot['lba'] = 1 if controller.left_bumper() and controller.a() else 0

            # # Right bumper combinations
            # robot['rbx'] = 1 if controller.right_bumper() and controller.x() else 0
            # robot['rby'] = 1 if controller.right_bumper() and controller.y() else 0
            # robot['rbb'] = 1 if controller.right_bumper() and controller.b() else 0
            # robot['rba'] = 1 if controller.right_bumper() and controller.a() else 0

            if(robot):
                print(robot)
                await websocket.send(pickle.dumps(robot))
                oldRobot = robot
            with suppress(asyncio.TimeoutError):
                response = await asyncio.wait_for(websocket.recv(), .1) #the number here is how fast it refreshes

    finally:
        await websocket.close()

def main():
    asyncio.get_event_loop().run_until_complete(SendMessage())

if __name__ == '__main__':
    main()