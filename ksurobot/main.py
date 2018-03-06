''' main.py

    Starts the program
'''

import asyncio
import websockets
import logging
from server import Server
from robot import Robot
from settings import *


def main():
    ''' Main Entrance to the program '''

    # Setup Logging
    logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Get the event loop to work with
    loop = asyncio.get_event_loop()

    # Setup Robot
    robot = Robot()

    server = Server(SERVER_IP, SERVER_PORT, robot)

    try:
        # Main event loop
        loop.run_until_complete(server.start_server())
        loop.run_forever()

    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt. Closing...')

    finally:
        # Shutdown the server
        task = asyncio.ensure_future(server.shutdown())
        loop.run_until_complete(task)

        # Close the loop
        loop.close()
        logger.info('Event loop closed')


if __name__ == '__main__':
    main()
