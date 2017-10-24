'''
Robot.py

This is the main controller file

'''

import asyncio
import websockets
import logging
from Server import Server


port = 8055
ip = '127.0.0.1'

def main():
    '''
        Main Entrance to the program
    '''
    # Setup Logging
    # Debug Mode
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    # Production Mode
    # logging.basicConfig(filename='log.log', format='%(asctime)s %(message)s', level=logging.INFO)

    try:
        server = Server(ip, port)
        asyncio.get_event_loop().run_until_complete(server.start_server())
        asyncio.get_event_loop().run_forever()
    except:
        # rightMotor.set_all_pwm(0, 0)
        # leftMotor.set_all_pwm(0, 0)
        print('broken')
        asyncio.get_event_loop().close()


if __name__ == '__main__':
    main()