"""Nodes representing operators"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['BlockNode', 'ForLoopNode', 'WhileLoopNode', 'IfNode']

from typing import Optional

from library.interpreter.nodes import Node
from library.interpreter.variables import Context, Value


class BlockNode(Node):
    """Represents a block of statements"""

    def __init__(self, children: list[Node]) -> None:
        self.children = children

    def evaluate(self, context: Context) -> list[Optional[Value]]:
        """Evaluate the statements in the block"""
        return [c.evaluate(context) for c in self.children]


class ForLoopNode(Node):
    """Represents a for loop"""

    def __init__(self, init: Node, check: Node, change: Node, body: Node) -> None:
        self.init = init
        self.check = check
        self.change = change
        self.body = body

    def evaluate(self, context: Context) -> Optional[Value]:
        """Evaluate the for loop"""
        with context:
            self.init.evaluate(context)
            while self.check.evaluate(context).value:
                with context:
                    self.body.evaluate(context)
                self.change.evaluate(context)
        return None


class WhileLoopNode(Node):
    """Represents a for loop"""

    def __init__(self, check: Node, body: Node) -> None:
        self.check = check
        self.body = body

    def evaluate(self, context: Context) -> Optional[Value]:
        """Evaluate the while loop"""
        with context:
            while self.check.evaluate(context).value:
                with context:
                    self.body.evaluate(context)
        return None


class IfNode(Node):
    """Represents an if statement"""

    def __init__(self, check: Node, body: Node, else_: Node) -> None:
        self.check = check
        self.body = body
        self.else_ = else_

    def evaluate(self, context: Context) -> Optional[Value]:
        """Evaluate the if statements"""
        if self.check.evaluate(context).value:
            with context:
                self.body.evaluate(context)
        else:
            with context:
                self.else_.evaluate(context)
        return None
