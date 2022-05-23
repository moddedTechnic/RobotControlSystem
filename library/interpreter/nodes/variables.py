"""Nodes representing variables and functions"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['NonLocalVariableNode', 'VariableDeclarationNode', 'VariableDefinitionNode', 'VariableAccessNode']

from typing import Optional

from library.interpreter.nodes import Node
from library.interpreter.variables import Type, Context, Value, Integer, true, false, null, undefined


class NonLocalVariableNode(Node):
    """Marks a variable as being non-local"""

    def __init__(self, name: str) -> None:
        self.name = name

    def evaluate(self, context: Context):
        """Make the variable nonlocal"""
        context.declare(self.name, type(Context.NONLOCAL), Context.NONLOCAL)


class VariableDeclarationNode(Node):
    """Represents a variable declaration"""

    def __init__(self, name: str, typ_name: str | None, child: Optional[Node] = None, *, const: bool = False) -> None:
        self.name = name
        self.typ_name = typ_name
        self.child = child
        self.const = const

    def __repr__(self) -> str:
        typ_name = 'auto' if self.typ_name is None else self.typ_name
        return f'{type(self).__name__}{self.name, typ_name, self.child}'

    def evaluate(self, context: Context):
        """Evaluate the node"""
        value = undefined if self.child is None else self.child.evaluate(context)
        if value is undefined and self.typ_name is None:
            raise TypeError('Cannot infer the type of "undefined"')
        typ = value.typ if self.typ_name is None else context[self.typ_name]
        if not (isinstance(typ, Type) or (isinstance(typ, type) and issubclass(typ, Value))):
            raise TypeError(f'Cannot create a variable of type "{typ}" - it is not a type')
        if self.child is None:
            return context.declare(self.name, typ, const=self.const)
        context.declare(self.name, typ, value, const=self.const)


class VariableDefinitionNode(Node):
    """Represents a variable definition"""

    def __init__(self, name: str, child: Node) -> None:
        self.name = name
        self.child = child

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.name}, {self.child})'

    def evaluate(self, context: Context):
        """Define the variable"""
        context[self.name] = self.child.evaluate(context)


class VariableAccessNode(Node):
    """Represents accessing a variable"""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.name})'

    def evaluate(self, context: Context):
        """Retrieve the value of the variable from the context"""
        if self.name in context.peek():
            return context[self.name]
        if self.name.isdigit():
            return Integer(self.name)
        if self.name == 'true':
            return true
        if self.name == 'false':
            return false
        if self.name == 'null':
            return null
        if self.name == 'undefined':
            return undefined
        return context[self.name]
