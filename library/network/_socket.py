"""A wrapper around the Python socket library"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Address', 'Connection', 'Socket']

import socket
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import Union, Optional, NamedTuple

from . import default_settings
from .message import Message, MessageType


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

    def send(self, message: Message, target: Union[socket.socket, Connection, None] = None) -> bool:
        """Send a message to either `target` or the current socket"""
        if target is None:
            target = self.socket
        if isinstance(target, Connection):
            target = target.connection
        header, body = message.transmission_chunks
        header_bytes = header.encode(default_settings.ENCODING)
        header_length = len(header_bytes).to_bytes(2, 'big')
        target.send(header_length)
        target.send(header_bytes)
        if body is not None:
            target.send(body.encode(default_settings.ENCODING))
        return True

    def receive(self, target: Union[socket.socket, Connection, None] = None) -> Optional[Message]:
        """Receive a message from either `target` or the current socket"""
        if target is None:
            target = self.socket
        if isinstance(target, Connection):
            target = target.connection
        header_length = int.from_bytes(target.recv(2), 'big')
        header_bytes = target.recv(header_length)
        headers = dict(map(
            lambda x: (x[0].strip(), x[1].strip()),
            map(partial(str.split, sep=':'), header_bytes.decode(default_settings.ENCODING).split('\n'))
        ))
        if 'message-type' not in headers:
            return None  # if we don't know what the content type is, we can't handle the message
        message_type = MessageType.from_name(headers['message-type'])
        if message_type is MessageType.DISCONNECT:
            return Message.disconnect()
        if message_type.has_body:
            message_length = int(headers['message-length'])
            body = target.recv(message_length).decode(default_settings.ENCODING)
            return Message(message_type, body)
        return None
