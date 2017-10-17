'''
Server

This is the server to be ran on the pi

'''
import asyncio
import websockets
import pickle

# Logging
from logging import Logger
logger = Logger(__name__)


class Server(object):
    ''' 
    Defines a server object to handle connections
    '''

    def __init__(self, ip, port):
        '''
        Construct a server with 
        '''
        self._active_connections = set()
        self.ip = ip
        self.port = port

    async def start_server(self):
        logger.info('server starting up')
        self.server = await websockets.serve(self.handle_new_connection, self.ip, self.port, timeout=1)

    async def handle_new_connection(self, ws, path):
        logger.debug('new connection to server')