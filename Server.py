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

    def __init__(self, ip, port):
        '''
            Construct a server with an ip on a port
        '''
        self._active_connections = set()
        self.ip = ip
        self.port = port

    async def start_server(self):
        '''
            Start the server
        '''
        logging.info('Server starting up')
        self.server = await websockets.serve(self.handle_new_connection, self.ip, self.port, timeout=1)

    async def handle_new_connection(self, ws, path):
        '''
            Handle a new incoming connection to the server
        '''
        global p

        logging.info('New connection to server')
        self._active_connections.add(ws)
        
        # Test the new connection
        # _thread.start_new(self.test_connection, ())

        # Run forever until connection is lost
        while True:
            if p == 2: # check if connection has been lost
                # Stop the robot
                # Need actual code to stop the robot
                quit()
            else:
                # Wait for a message
                result = await ws.recv()
            await self.handle_msg(result)
        self._active_connections.remove(ws)

    async def handle_msg(self, msg):
        logging.info(pickle.loads(msg))

    async def send(self, msg):
        logging.info("Sending a messgage")
        try:
            for ws in self._active_connections:
                asyncio.ensure_future(ws.send(msg))
        except:
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