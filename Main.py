''' Main.py

    This is the main controller file
'''

import asyncio
import websockets
import logging
from Server import Server
from Robot import Robot
from Settings import *


def main():
    ''' Main Entrance to the program '''

    # Setup Logging
    logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.DEBUG)
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
        logger.warn('Keyboard Interrupt. Closing Connections...')

    finally:
        # Stop the Robot
        robot.stop()
        logger.info('Robot stopped')

        # Shutdown the server
        task = asyncio.ensure_future(server.shutdown())
        loop.run_until_complete(task)

        # Close the loop
        loop.close()
        logger.info('Event loop closed')


if __name__ == '__main__':
    main()
