"""Default settings for the network"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = []

import socket

HOST_NAME: str = 'localhost'
PORT: int = 8080
SERVER: str = socket.gethostbyname(HOST_NAME)

ENCODING: str = 'utf-8'
