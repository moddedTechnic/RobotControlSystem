"""A base class representing a server"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Server', 'MessageHandler']

import socket
import sys
import traceback
from typing import Callable

from ._socket import Address, Connection, Socket
from .message import MessageType, Message


MessageHandler = Callable[[Message], None]


class Server(Socket):
    """Represents a network server"""

    def __init__(self, message_handler: MessageHandler, /, *, hostname: str = None, port: int = None) -> None:
        super().__init__(hostname, port)
        self.connections: dict[Address, Connection] = {}
        self.process_message = message_handler

    def connect(self) -> None:
        """Connect the server to the appropriate address"""
        self.socket.bind(self.address)

    def disconnect(self) -> None:
        """Disconnect the server from the appropriate address"""
        self.socket.detach()

    def start(self):
        """Start the server"""
        self.connect()
        print('[STARTING] The server is starting...')
        self.socket.listen()
        print(f'[LISTENING] The server is listening on {self.address}')
        while True:
            try:
                conn, address = self.socket.accept()
                self.connect_client(conn, Address(*address))
            except KeyboardInterrupt:
                break
            except Exception as ex:
                print(*traceback.format_exception(type(ex), ex, ex.__traceback__), sep='', file=sys.stderr)

    def connect_client(self, conn: socket.socket, address: Address) -> None:
        """Connect a client to the server"""
        print(f'[NEW CONNECTION] {address} connected to the server')
        connection = Connection(address, conn, connected=True)
        self.connections[address] = connection
        while self.connections[address].connected:
            self.handle_client(connection)
        conn.close()

    def handle_client(self, connection: Connection) -> None:
        """Handle a client message"""
        msg = self.receive(target=connection)
        if msg is None:
            return
        if msg.type is MessageType.DISCONNECT:
            self.connections[connection.address].connected = False
            return
        self.process_message(msg)
