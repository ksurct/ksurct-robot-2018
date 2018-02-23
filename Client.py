''' Client.py

    Send controller info to the server
'''

import websockets
import asyncio
from contextlib import suppress
from concurrent.futures import CancelledError
from xbox import Controller
import pickle

import logging

logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

IP = '129.130.46.4'
PORT = 8055

DELAY_TIME = 1

# Initalize controller number 0
Controller.init()
controller = Controller(0)

async def SendMessage():
    '''
        Send the state of the controller to the server
    '''
    
    # Try to reconect to the server on failure
    while True:
        try:
            websocket = await websockets.connect('ws://{0}:{1}'.format(IP, PORT))
        except ConnectionRefusedError:
            logger.warn('Connection Refused at {0}:{1}, trying again'.format(IP, PORT))
            await asyncio.sleep(DELAY_TIME)
        else:
            break
    
    logger.info('Connected to server at: {0}'.format(str(websocket.remote_address)))

    # Create the dictionary to send
    robot = {}

    try:
        while True:
            # update the controller object
            controller.update()

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

            # Send the robot state
            if(robot):
                logger.debug('Sending: {}'.format(robot))
                await websocket.send(pickle.dumps(robot))
            with suppress(asyncio.TimeoutError):
                response = await asyncio.wait_for(websocket.recv(), .1) #the number here is how fast it refreshes
    
    except CancelledError:
        pass
    except websockets.ConnectionClosed:
        logger.info('Server closed connection')
    finally:
        # Close the connection
        await websocket.close()
        logger.info('Connection closed to: {}'.format(websocket.remote_address))

def main():
    loop = asyncio.get_event_loop()
    try:
        current_task = asyncio.ensure_future(SendMessage())
        loop.run_until_complete(current_task)
    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt. Closing Connection...')
        
        # Cancel tasks
        current_task.cancel() # Set task to be cancelled
        loop.run_forever() # This line actually cancels the task

    finally:
        loop.close()

if __name__ == '__main__':
    main()
