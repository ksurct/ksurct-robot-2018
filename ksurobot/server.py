''' server.py

    This is the server to be ran on the pi
'''
import asyncio
import pickle
import logging
import websockets


class TextColors:
    '''
        Set of definitions for terminal text color
    '''
    WARN = '\033[93m'	# Color used for warnings!
    CONF = '\033[94m'	# Color used for confirmations
    PRINT = '\033[92m'	# Color used to distinguish the standard output of p
    BOLD = '\033[1m'	# Bold text to amplify textclass textColors


class Server(object):
    ''' Defines a server object to handle connections '''

    def __init__(self, ip, port, robot):
        ''' Construct a server with an ip on a port '''

        self._active_connections = set()
        self.ip = ip
        self.port = port
        self.logger = logging.getLogger('__main__')
        self.server = None
        self.robot = robot

    async def start_server(self):
        ''' Start the server on the defined ip and port '''

        self.logger.info('Server starting up at {0}:{1}'.format(self.ip, self.port))
        self.server = await websockets.serve(self.handle_new_connection, self.ip, self.port, timeout=1)

    async def handle_new_connection(self, ws, path):
        ''' Handle a new incoming connection to the server '''

        # Note the new connection
        self.logger.info('New connection to server from: {0}'.format(str(ws.remote_address)))
        # Add the connection to the set
        self._active_connections.add(ws)

        # Create tasks to run in the event loop
        try:
            consumer_task = asyncio.ensure_future(self.consumer_handler(ws))
            producer_task = asyncio.ensure_future(self.producer_handler(ws))

            await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_EXCEPTION)

        except websockets.ConnectionClosed:
            self.logger.info('Connection already closed')
        finally:
            # Stop robot
            self.logger.info('Stopping Robot')
            self.stop()

            # Close Connection
            if ws.open:
                await ws.close()
                self.logger.info('Closed connection: {}'.format(ws.remote_address))

            # Remove connection
            self._active_connections.remove(ws)
            self.logger.info('Connection removed: {}'.format(ws.remote_address))

    async def consumer_handler(self, ws):
        ''' Waits for a message from the client and
            passes that message to the robot, if it exsits
        '''
        while True:
            # Receive the message
            pickled_message = await ws.recv()

            # Use pickle to load the message
            message = pickle.loads(pickled_message)

            self.logger.info('Recieved: {}'.format(message))

            # Update the robot if it exsits
            if self.robot:
                await self.robot.update(message)

    async def producer_handler(self, ws):
        ''' Waits for the robot to produce a message
            and then sends that message to the client
        '''
        while True:
            # Get the message from the robot, if it exsits
            if self.robot:
                message = await self.robot.produce()

                self.logger.info("Sending: {}".format(message))

                # Use pickle to package the message
                pickled_message = pickle.dumps(message)

                # Send the message
                await ws.send(pickled_message)
            await asyncio.sleep(.5)


    async def shutdown(self):
        ''' Shutdown the server if it exsits '''
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    def stop(self):
        ''' Stop the robot if it exsits '''
        if self.robot:
            self.robot.stop()

def test_server():
    ''' Sets up a test server with robot set to none on localhost for testing '''

    ip = '127.0.0.1' # localhost
    port = 8055

    # Setup logging
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Create server object
    server = Server(ip, port, None)

    try:
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
    test_server()
