"""Nodes representing operators"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = []

from typing import Type as PyType

from library.interpreter.nodes import Node
from library.interpreter.nodes.variables import VariableAccessNode
from library.interpreter.variables import Context, Value


class UnaryOperatorNode(Node):
    """Represents a unary operator"""

    name: str = None
    op: str = None

    def __init__(self, child: Node) -> None:
        self.child = child

    def evaluate(self, context: Context) -> Value:
        """Evaluate the unary operation"""
        a = self.child.evaluate(context)
        handler_name = f'unary_operator_{self.name}'
        if hasattr(a, handler_name):
            handler = getattr(a, handler_name)
            if (result := handler.call(a)) is not NotImplemented:
                return result
        raise TypeError(
            f'bad operand type for {self.op}: "{type(a).__name__}"'
        )


def _make_unary_operator(name: str, op: str) -> PyType[UnaryOperatorNode]:
    typ_name = ''.join(n.capitalize() for n in name.split('_')) + 'OperatorNode'
    typ = type(typ_name, (UnaryOperatorNode,), {'name': name, 'op': op})
    __all__.append(typ)
    # noinspection PyTypeChecker
    return typ


UnaryPlusOperatorNode = _make_unary_operator('plus', '+')
UnaryMinusOperatorNode = _make_unary_operator('minus', '+')


class IncrementOperatorNode(Node):
    """Represents the increment operator"""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.name})'

    def evaluate(self, context: Context) -> Value:
        """Evaluate the unary operation"""
        a = context[self.name]
        handler_name = 'unary_operator_increment'
        if hasattr(a, handler_name):
            handler = getattr(a, handler_name)
            if (result := handler.call(a)) is not NotImplemented:
                context[self.name] = result
                return result
        raise TypeError(
            f'bad operand type for ++: "{type(a).__name__}"'
        )


class DecrementOperatorNode(Node):
    """Represents the increment operator"""

    def __init__(self, name: str) -> None:
        self.name = name

    def evaluate(self, context: Context) -> Value:
        """Evaluate the unary operation"""
        a = context[self.name]
        handler_name = 'unary_operator_decrement'
        if hasattr(a, handler_name):
            handler = getattr(a, handler_name)
            if (result := handler.call(a)) is not NotImplemented:
                context[self.name] = result
                return result
        raise TypeError(
            f'bad operand type for --: "{type(a).__name__}"'
        )


class BinaryOperatorNode(Node):
    """Represents a unary operator"""

    name: str = None
    op: str = None

    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

    def evaluate(self, context: Context) -> Value:
        """Evaluate the binary operation"""
        a = self.left.evaluate(context)
        b = self.right.evaluate(context)
        handler_name = f'operator_{self.name}'
        if hasattr(a, handler_name):
            handler = getattr(a, handler_name)
            if (result := handler.call(a, b)) is not NotImplemented:
                return result
        reverse_handler_name = f'reverse_operator_{self.name}'
        if hasattr(b, reverse_handler_name):
            reverse_handler = getattr(b, reverse_handler_name)
            if (result := reverse_handler.call(b, a)) is not NotImplemented:
                return result
        raise TypeError(
            f'unsupported operand type(s) for {self.op}: "{type(a).__name__}" and "{type(b).__name__}"'
        )


def _make_binary_operator(name: str, op: str) -> PyType[BinaryOperatorNode]:
    typ_name = ''.join(n.capitalize() for n in name.split('_')) + 'OperatorNode'
    typ = type(typ_name, (BinaryOperatorNode,), {'name': name, 'op': op})
    __all__.append(typ)
    # noinspection PyTypeChecker
    return typ


PlusOperatorNode = _make_binary_operator('plus', '+')
MinusOperatorNode = _make_binary_operator('minus', '-')
StarOperatorNode = _make_binary_operator('star', '*')
SlashOperatorNode = _make_binary_operator('slash', '/')


class ComparisonOperatorNode(BinaryOperatorNode):
    """Represents a comparison operator"""

    back_name: str = None

    def evaluate(self, context: Context):
        """Evaluate the comparison operation"""
        a = self.left.evaluate(context)
        b = self.right.evaluate(context)
        handler_name = f'operator_{self.name}'
        if hasattr(a, handler_name):
            handler = getattr(a, handler_name)
            if (result := handler.call(a, b)) is not NotImplemented:
                return result
        back_handler_name = f'operator_{self.back_name}'
        if hasattr(b, back_handler_name):
            back_handler = getattr(b, back_handler_name)
            if (result := back_handler.call(b, a)) is not NotImplemented:
                return result
        raise TypeError(
            f'unsupported operand type(s) for {self.op}: "{type(a).__name__}" and "{type(b).__name__}"'
        )


def _make_comparison_operator(name: str, back_name: str, op: str) -> PyType[ComparisonOperatorNode]:
    typ_name = ''.join(n.capitalize() for n in name.split('_')) + 'OperatorNode'
    typ = type(typ_name, (ComparisonOperatorNode,), {'name': name, 'back_name': back_name, 'op': op})
    __all__.append(typ)
    # noinspection PyTypeChecker
    return typ


LessOperatorNode = _make_comparison_operator('less', 'greater', '<')
LessEqualOperatorNode = _make_comparison_operator('less_equal', 'greater_equal', '<=')
GreaterOperatorNode = _make_comparison_operator('greater', 'less', '>')
GreaterEqualOperatorNode = _make_comparison_operator('greater_equal', 'less_equal', '>=')
EqualityOperatorNode = _make_comparison_operator('equality', 'equality', '==')
NonEqualityOperatorNode = _make_comparison_operator('nonequality', 'nonequality', '!=')


class AssignmentOperatorNode(Node):
    """Represents an assignment operator"""

    name: str = None
    op: str = None

    def __init__(self, variable_name: str, child: Node) -> None:
        self.variable_name = variable_name
        self.child = child

    def evaluate(self, context: Context):
        """Evaluate the operator"""
        a = context[self.variable_name]
        b = self.child.evaluate(context)
        handler_name = f'assignment_operator_{self.name}'
        if hasattr(a, handler_name):
            handler = getattr(a, handler_name)
            if (result := handler.call(a, b)) is not NotImplemented:
                context[self.variable_name] = result
                return result
        raise TypeError(
            f'unsupported operand type(s) for {self.op}=: "{type(a).__name__}" and "{type(b).__name__}"'
        )


def _make_assignment_operator(name: str, op: str) -> PyType[BinaryOperatorNode]:
    typ_name = ''.join(n.capitalize() for n in name.split('_')) + 'OperatorNode'
    typ = type(typ_name, (AssignmentOperatorNode,), {'name': name, 'op': op})
    __all__.append(typ)
    # noinspection PyTypeChecker
    return typ


PlusEqualsOperatorNode = _make_assignment_operator('plus', '+')
MinusEqualsOperatorNode = _make_assignment_operator('minus', '-')
StarEqualsOperatorNode = _make_assignment_operator('star', '*')
SlashEqualsOperatorNode = _make_assignment_operator('slash', '/')


class DotOperatorNode(Node):
    """Represents a dot operation"""

    GET = object()
    SET = object()

    def __init__(self, left: Node, right: Node, mode=GET) -> None:
        self.left = left
        self.right = right
        self.mode = mode

    def evaluate(self, context: Context):
        """Evaluate the node"""
        if self.mode is self.GET:
            left = self.left.evaluate(context)
            if isinstance(self.right, VariableAccessNode):
                right = self.right.name
            else:
                right = self.right.evaluate(context)
            if hasattr(left, 'operator_get'):
                return left.operator_get.call(left, right)
            raise NameError(f'Cannot get {right} from {left}')
        if self.mode is self.SET:
            print('Setting', self.left, 'DOT', self.right)

