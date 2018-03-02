''' client.py

    Send controller info to the server
'''

import websockets
import asyncio
from contextlib import suppress
from concurrent.futures import CancelledError
from xbox import Controller
import pickle
import logging

from settings import SERVER_IP, SERVER_PORT

TIMEOUT_DELAY = 5
DELAY_TIME = 1


class Client(object):

    def __init__(self, ip, port):

        # Initalize controller number 0
        Controller.init()
        self.controller = Controller(0)
        self.logger = logging.getLogger(__name__)
        self.ws = None
        self.ip = ip
        self.port = port

    async def start_client(self):
        ''' Setup Client '''
        # while True:
        await self.connect()
        await self.handle_connection()

    async def connect(self):
        ''' Connect to server at ip and port, try to reconect on failure '''
        while True:
            try:
                ws = await asyncio.wait_for(websockets.connect('ws://{0}:{1}'.format(self.ip, self.port)), TIMEOUT_DELAY)
            except ConnectionRefusedError:
                self.logger.info('Connection Refused at {0}:{1}, trying again'.format(self.ip, self.port))
                await asyncio.sleep(DELAY_TIME)
            except asyncio.TimeoutError:
                self.logger.info('Connection to {0}:{1} timed out, trying again'.format(self.ip, self.port))
            else:
                if ws.open:
                    self.logger.info('Connected to server at: {0}'.format(str(ws.remote_address)))
                    self.ws = ws
                    return

    async def handle_connection(self):
        ''' Maintain send and receive task with the server '''
        while True:
            try:
                sender_task = asyncio.ensure_future(self.sender())
                receiver_task = asyncio.ensure_future(self.receiver())

                await asyncio.wait([sender_task, receiver_task], return_when=asyncio.FIRST_EXCEPTION)

            except CancelledError:
                pass

            except websockets.ConnectionClosed:
                # Close the connection
                self.logger.info('Server closed connection')
                if self.ws.open:
                    await self.ws.close()
                self.logger.info('Connection closed to: {}'.format(self.ws.remote_address))
                break

#            finally:
            await self.connect()

    async def sender(self):
        ''' Handle data that needs to be sent to the server '''
        while self.ws.open:
            # Get updated controller data
            controller_data = self.get_controller_data()

            if controller_data:
                self.logger.info('Sending: {}'.format(controller_data))

                pickled_message = pickle.dumps(controller_data)

                await self.ws.send(pickled_message)
            await asyncio.sleep(1)

    async def receiver(self):
        ''' Handle data from the server '''
        while self.ws.open:
            # Get data from server
            pickled_message = await self.ws.recv()

            message = pickle.loads(pickled_message)

            self.logger.info('Received: {}'.format(message))

    async def shutdown(self):
        if ws.open:
            await ws.close()

    def get_controller_data(self):
        # Create the dictionary to send
        controller_data = {}

        # update the controller object
        self.controller.update()

        # General buttons
        controller_data['x'] = 1 if self.controller.x() else 0
        controller_data['y'] = 1 if self.controller.y() else 0
        controller_data['a'] = 1 if self.controller.a() else 0
        controller_data['b'] = 1 if self.controller.b() else 0

        # Triggers
        controller_data['r_trigger'] = int(self.controller.right_trigger() >> 3)
        controller_data['l_trigger'] = int(self.controller.left_trigger() >> 3)

        # Analog sticks
        r_stick_x = round(self.controller.right_x(), 1)
        r_stick_y = round(self.controller.right_y(), 1)
        l_stick_x = round(self.controller.left_x(), 1)
        l_stick_y = round(self.controller.left_y(), 1)
        controller_data['r_stick'] = (int(10*r_stick_x) if abs(r_stick_x) > 0.1 else 0,
                            int(-10*r_stick_y) if abs(r_stick_y) > 0.1 else 0 )
        controller_data['l_stick'] = (int(10*l_stick_x) if abs(l_stick_x) > 0.1 else 0,
                            int(-10*l_stick_y) if abs(l_stick_y) > 0.1 else 0 )

        # Bumpers
        controller_data['r_bump'] = 1 if self.controller.right_bumper() else 0
        controller_data['l_bump'] = 1 if self.controller.left_bumper() else 0

        # D-pad
        controller_data['left'] = 1 if str(self.controller.hat).strip() == 'l' else 0
        controller_data['right'] = 1 if str(self.controller.hat).strip() == 'r' else 0
        controller_data['up'] = 1 if str(self.controller.hat).strip() == 'u' else 0
        controller_data['down'] = 1 if str(self.controller.hat).strip() == 'd' else 0

        return controller_data


def main():

    # Setup Logging
    logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Get the event loop to work with
    loop = asyncio.get_event_loop()

    # Create client that will talk to the server
    client = Client(SERVER_IP, SERVER_PORT)

    try:
        current_task = asyncio.ensure_future(client.start_client())
        loop.run_until_complete(current_task)
    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt. Closing...')

        # Cancel tasks
        current_task.cancel() # Set task to be cancelled
#        loop.run_forever() # This line actually cancels the task

    finally:
        loop.close()

if __name__ == '__main__':
    main()
