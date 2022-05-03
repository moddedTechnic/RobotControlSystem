"""Run a server to receive commands to control the robot"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = []

import os
import sys
from pathlib import Path

__dir__ = Path(__file__).parent
sys.path.insert(0, os.fspath(__dir__))
sys.path.insert(1, os.fspath(__dir__.parent))

from library.network.server import Server
from library.network.message import Message, MessageType


def handle_message(send, message: Message) -> None:
    """Handle a message"""
    if message.type is MessageType.CODE:
        print('Received code:', message.body)


def main():
    """Put code here to be run when the module is run"""
    server = Server(handle_message)
    server.start()


if __name__ == '__main__':
    main()
