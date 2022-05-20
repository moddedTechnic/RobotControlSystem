"""This package contains a variety of nodes used in the construction of an abstract syntax tree"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Node']

from abc import ABC, abstractmethod
from typing import Optional

from library.interpreter.variables import Context, Value


class Node(ABC):
    """Represents a node in the AST"""

    @abstractmethod
    def evaluate(self, context: Context) -> Optional[Value]:
        """Evaluate the node"""
