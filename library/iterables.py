"""Utilities relating to iterables"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['first']

from typing import Union, TypeVar

T = TypeVar('T')


def first(it: Union[tuple[T], list[T]]) -> T:
    """Get the first item of the iterable"""
    return it[0]
