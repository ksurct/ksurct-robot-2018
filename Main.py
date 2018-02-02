'''
Robot.py

This is the main controller file

'''

import asyncio
import websockets
import logging
from Server import Server
from Robot import Robot
from Settings import *


def main():
    '''
        Main Entrance to the program
    '''
    # Setup Logging
    # Debug Mode
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    # Production Mode
    # logging.basicConfig(filename='log.log', format='%(asctime)s %(message)s', level=logging.INFO)

    # Setup Robot
    robot = Robot()

    try:
        server = Server(SERVER_IP, SERVER_PORT, robot)
        asyncio.get_event_loop().run_until_complete(server.start_server())
        asyncio.get_event_loop().run_forever()
    except:
        asyncio.get_event_loop().close()
        logging.info("Closing")
        quit()


if __name__ == '__main__':
    main()