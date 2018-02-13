'''
Server.py

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
    '''
        Defines a server object to handle connections
    '''

    def __init__(self, ip, port, robot):
        '''
            Construct a server with an ip on a port
        '''
        self._active_connections = set()
        self.ip = ip
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.server = None
        self.robot = robot

    async def start_server(self):
        '''
            Start the server on the defined ip and port
        '''
        self.logger.info('Server starting up at {0}:{1}'.format(self.ip, self.port))
        self.server = await websockets.serve(self.handle_new_connection, self.ip, self.port, timeout=1)

    async def handle_new_connection(self, ws, path):
        '''
            Handle a new incoming connection to the server
        '''

        # Note the new connection
        self.logger.info('New connection to server: {0}'.format(str(ws)))
        # Add the connection to the set
        self._active_connections.add(ws)
        # Set status to alive
        alive = True

        # Create tasks to run in the event loop
        consumer_task = asyncio.ensure_future(ws.recv())
        producer_task = asyncio.ensure_future(self.robot.produce())
        
        # Run forever until connection is lost
        try:
            while alive:
                # Wait for the first task to be completed
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                # If consumer task is completed,
                if consumer_task in done:
                    # Get message from the task
                    message = consumer_task.result()
                    self.logger.debug(message)
                    if message is not None:
                        # Load from the pickle and handle the message
                        self.handle_msg(pickle.loads(message))
                        # Create a new task to be run in the event loop
                        listener_task = asyncio.ensure_future(ws.recv())
                    else:
                        # Kill the connection
                        alive = False
                # If producer task is completed,
                if producer_task in done:
                    # Get the message from the task
                    message = producer_task.result()
                    # Check that the connection is still available
                    if ws.open:
                        # Send the mesage to the client
                        await ws.send(pickle.dumps(message))
                        producer_task = asyncio.ensure_future(self.robot.produce())
                    else:
                        alive = False
        finally:
            # Stop robot
            self.stop()
            self.logger.info('Robot stopped')

            # Close Connection
            if ws.open:
                await ws.close()
            self.logger.info('Connection closed: {}'.format(ws.remote_address))
            
            # Remove connection
            self._active_connections.remove(ws)
            self.logger.info('Connection removed: {}'.format(ws.remote_address))

    async def consumer_handler(self, ws): # Unused right now
        '''
            Awaits for a message from the client and
            passes that message to the robot, if it exsits
        '''

        while True:
            # Receive the message
            pickled_message = await websocket.recv()

            # Use pickle to load the message
            message = pickle.loads(pickled_message)

            self.logger.debug('Recieved: {}'.format(message))
            
            # Update the robot if it exsits
            if self.robot:
                await self.robot.update(pickle.loads(message))
    
    async def producer_handler(self, ws): # Unused right now
        '''
            Awaits for the robot to produce a message
            and then sends that message to the client
        '''
        
        while True:
            # Get the message from the robot, if it exsits
            if self.robot:
                message = await self.robot.produce()

            self.logger.debug("Sending: {}".format(message))

            # Use pickle to package the message
            pickled_message = pickle.dumps(message)

            # Send the message
            await ws.send(pickled_message)

    async def send(self, msg): # Unused right now
        try:
            self.logger.debug("Sending: {}".format(msg))
            for ws in self._active_connections:
                asyncio.ensure_future(ws.send(msg))
        except:
            self.logger.info('Send failed')
            # self._active_connections = set()
            # asyncio.get_event_loop().close()
    
    async def shutdown(self):
        '''
            Shutdown the server if it exsits
        '''

        if self.server:
            self.server.close()
            await self.server.wait_closed()
    
    def stop(self):
        '''
            Stop the robot if it exsits
        '''

        if self.robot:
            self.logger.info("Stopping the Robot")
            self.robot.stop()
        
def test_server():
    '''
        Sets up a test server with robot set to none on localhost for testing
    '''
    
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
        logger.info('Keyboard Interrupt. Closing Connections...')
    
    finally:
        # Shutdown the server
        task = asyncio.ensure_future(server.shutdown())
        loop.run_until_complete(task)

        # Close the loop
        loop.close()
        logger.info('Event loop closed')

if __name__ == '_