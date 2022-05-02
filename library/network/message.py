"""Utilities for representing a message to be transmitted"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Message', 'MessageType']

from dataclasses import dataclass, field
from typing import Optional, Iterable

from library.network.default_settings import ENCODING


class _MessageTypeMeta(type):
    def __iter__(cls) -> Iterable['MessageType']:
        for k, v in cls.__dict__.items():
            if k.isupper():
                yield v


@dataclass
class MessageType(metaclass=_MessageTypeMeta):
    """Represents the different types of message"""
    name: str
    has_body: bool = True

    CODE: 'MessageType' = field(default=None, init=False, repr=False)
    DISCONNECT: 'MessageType' = field(default=None, init=False, repr=False)
    FILE: 'MessageType' = field(default=None, init=False, repr=False)

    @classmethod
    def from_name(cls, name: str) -> 'MessageType':
        """Get a message type with the given name"""
        for typ in cls:
            if typ.name == name:
                return typ
        raise NameError(f'{name} was not found in {cls.__name__}')


MessageType.CODE = MessageType('code')
MessageType.DISCONNECT = MessageType('disconnect', has_body=False)
MessageType.FILE = MessageType('file')


class Message:
    """Represents a message"""

    def __init__(self, typ: MessageType, body: Optional[str] = None):
        self.type = typ
        self.body = body

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.type}, body={self.body})'

    @property
    def transmission_chunks(self) -> tuple[str, Optional[str]]:
        """Get the chunks to transmit the message in"""
        headers = f'message-type: {self.type.name}\n'
        if self.type.has_body:
            headers += f'message-length: {len(self.body.encode(ENCODING))}'
        headers = headers.strip()
        if self.type.has_body:
            return headers, self.body
        return headers, None

    @classmethod
    def code(cls, body: str):
        """A message representing a code string"""
        return cls(MessageType.CODE, body)

    @classmethod
    def file(cls, body: str):
        """A message representing the contents of a file"""
        return cls(MessageType.FILE, body)

    @classmethod
    def disconnect(cls):
        """A message instructing the server to disconnect"""
        return cls(MessageType.DISCONNECT)
