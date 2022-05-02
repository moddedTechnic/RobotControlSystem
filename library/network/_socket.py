"""A wrapper around the Python socket library"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Address', 'Connection', 'Socket']

import socket
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, Optional, NamedTuple

from . import default_settings


class Address(NamedTuple):
    """Represents an address (host, port pair)"""
    hostname: str
    port: int

    def __str__(self) -> str:
        return f'{self.hostname}:{self.port}'


@dataclass
class Connection:
    """Represents a network connection"""
    address: Address
    connection: socket.socket
    connected: bool = False


class Socket(ABC):
    """Represents a socket and contains base abstractions for common functionality"""

    def __init__(self, hostname: str = None, port: int = None) -> None:
        hostname = default_settings.HOST_NAME if hostname is None else hostname
        port = default_settings.PORT if port is None else port
        self.socket = socket.socket()
        self.address = Address(hostname, port)
        self.encoding = default_settings.ENCODING
        self.is_end_of_transmission = False

    @abstractmethod
    def connect(self) -> None:
        """Connect to the server"""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the server"""

    def send(self, message: str, target: Union[socket.socket, Connection, None] = None) -> bool:
        """Send a message to either `target` or the current socket"""
        if target is None:
            target = self.socket
        if isinstance(target, Connection):
            target = target.connection
        raise NotImplementedError
        return False

    def receive(self, target: Union[socket.socket, Connection, None] = None) -> Optional[str]:
        """Receive a message from either `target` or the current socket"""
        if target is None:
            target = self.socket
        if isinstance(target, Connection):
            target = target.connection
        raise NotImplementedError
        return None
