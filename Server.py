'''
Server

This is the server to be ran on the pi
'''
import asyncio
import pickle
import logging
import websockets

p = 1

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
        self.robot = robot

    async def start_server(self):
        '''
            Start the server
        '''
        logging.info('Server starting up at {0}:{1}'.format(self.ip, self.port))
        self.server = await websockets.serve(self.handle_new_connection, self.ip, self.port, timeout=1)

    async def handle_new_connection(self, ws, path):
        '''
            Handle a new incoming connection to the server
        '''

        # Note the new connection
        logging.info('New connection to server: {0}'.format(str(ws)))
        # Add the connection to the set
        self._active_connections.add(ws)
        # Set status to alive
        alive = True

        # Create tasks to run in the event loop
        consumer_task = asyncio.ensure_future(ws.recv())
        producer_task = asyncio.ensure_future(self.robot.produce())
        
        # Run forever until connection is lost
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
                logging.debug(message)
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
        # Connection lost, stop the robot
        self.robot.stop()
        self._active_connections.remove(ws)

'''
    async def consumer_handler(self, ws, path):
        while True:
            message = await websocket.recv()
            await self.handle_msg(message)
    
    async def producer_handler(self, ws, path):
        while True:
            message = await self.robot.produce()
            await ws.send(pickle.dumps(message))
'''

    def handle_msg(self, msg):
        logging.info(msg)
        self.robot.update(msg)

    async def send(self, msg):
        try:
            logging.info("Sending a messgage")

            for ws in self._active_connections:
                asyncio.ensure_future(ws.send(msg))
        except:
            logging.info("Message send failure")
            self._active_connections = set()
            asyncio.get_event_loop().close()
        
def main():
    ip = '127.0.0.1'
    port = 8055
    
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    server = Server(ip, port)
    asyncio.get_event_loop().run_until_complete(server.start_server())
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()