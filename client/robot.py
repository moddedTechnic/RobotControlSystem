"""Items relating to client-side robot utilities"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Robot']

from typing import NamedTuple


class Robot(NamedTuple):
    """Represents robot information"""
    device: str
    name: str
    host: str

    def __str__(self) -> str:
        return f'{self.device} - {self.name}'
