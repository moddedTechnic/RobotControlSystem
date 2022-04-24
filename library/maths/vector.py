"""Represents vectors"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Vec2']

from dataclasses import dataclass
from typing import Union


Vec2Tuple = tuple[float, float]


@dataclass(frozen=True)
class Vec2:
    """Represents a 2D vector"""
    x: float
    y: float

    def __add__(self, other: Union['Vec2', Vec2Tuple]):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
            return self + self.from_tuple(other)
        return NotImplemented

    def __truediv__(self, other: float):
        if isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)

    def to_tuple(self) -> Vec2Tuple:
        """Convert the vector to a tuple"""
        return self.x, self.y

    @classmethod
    def from_tuple(cls, t: Vec2Tuple) -> 'Vec2':
        """Convert the tuple to a vector"""
        return Vec2(*t)
