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
oldRobot = {'john': 34, 'bob':99}


async def SendMessage():
    '''
        Send the state of the controller to the server
    '''
    #ws://127.0.0.1:8055/ # zerotier IP of server
    logging.debug('pre IP connect')
    websocket = await websockets.connect('ws://129.130.46.36:8055')
    logging.info('Sent message')
    try:
        while True:
            controller.update()
            l_stick = round(controller.left_x(), 1)
            r_stick = round(controller.right_y(), 1)
            robot = {}
            oldRobot = {}
            robot['x'] = 1 if controller.x() else 0
            robot['y'] = 1 if controller.y() else 0
            robot['a'] = 1 if controller.a() else 0
            robot['b'] = 1 if controller.b() else 0
            robot['fwd'] = int(controller.right_trigger() >> 3)  # To implement turning, we will want to grab the left stick and adjust Fwd/Rev appropriately.
            robot['rev'] = int(controller.left_trigger() >> 3)
            robot['lstick'] = int(10*l_stick) if abs(l_stick) > 0.1 else 0
            robot['vision'] = 1 if str(controller.hat).strip() == 'd' else 0
            robot['peek'] = 1 if str(controller.hat).strip() == 'u' else 0
            robot['rstick'] = int(-10*r_stick) if abs(r_stick) > 0.1 else 0
            robot['lbump'] = 1 if controller.left_bumper() else 0

            # This needs testing, but logic seems in order.
            robot['lbx'] = 1 if controller.left_bumper() and controller.x() else 0
            robot['lbb'] = 1 if controller.left_bumper() and controller.b() else 0
            robot['lby'] = 1 if controller.left_bumper() and controller.y() else 0
            robot['lba'] = 1 if controller.left_bumper() and controller.a() else 0
            robot['rby'] = 1 if controller.right_bumper() and controller.y() else 0
            robot['rba'] = 1 if controller.right_bumper() and controller.a() else 0
            # If leftStick.X < 0 then we want to trim off the left motor to turn left.
            # If leftStick.X > 0 then we want to trim off the right motor to turn right.
            robot['valid'] = 1  # Was testing not spamming controller but that is impossible.

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