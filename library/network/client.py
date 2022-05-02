"""A base class representing a client"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Client']

from library.network._socket import Socket
from library.network.message import Message


class Client(Socket):
    """Represents a network client"""

    def connect(self) -> None:
        """Connect to the server"""
        self.socket.connect(self.address)

    def disconnect(self) -> None:
        """Disconnect from the server"""
        self.send(Message.disconnect())
