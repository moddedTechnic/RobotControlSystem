"""Items relating to the storage of variables and functions"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Integer', 'Rational']

from dataclasses import dataclass
from typing import Any, Union, Optional, Callable

from library import maths

from .nodes import Node


class Type:
    pass


@dataclass
class Value:
    typ: Union[type, Type]
    value: Any


class Signature:
    """Represents a function signature"""


class Arguments:
    """Represents a collection of arguments passed to a function"""


class Function(Value):
    """Represents a function in the context"""

    def __init__(self, signature: Signature, body: list[Node] | Callable):
        super().__init__(type(self), None)
        self.signature = signature
        self.body = body

    def call(self, *arguments):
        """Call the function"""
        if callable(self.body):
            return self.body(*arguments)
        raise NotImplementedError

    @classmethod
    def from_native(cls, func: Callable):
        """Create a function from a Python function"""
        return cls(Signature(), func)


class Rational(Value):
    """Represents a rational number"""

    def __init__(self, numerator: int, denominator: int):
        gcd = maths.gcd(numerator, denominator)
        self.numerator = numerator // gcd
        self.denominator = denominator // gcd
        if self.denominator == 0:
            raise ZeroDivisionError(f'Attempted to divide {numerator} by 0')

    def __repr__(self):
        return f'{self.numerator} / {self.denominator}'

    def as_tuple(self) -> tuple[int, int]:
        """Convert the number to a tuple (numerator, denominator)"""
        return self.numerator, self.denominator

    @Function.from_native
    def operator_plus(self, other: 'Integer | Rational') -> 'Rational':
        """Override the addition operator for integers"""
        if isinstance(other, Rational):
            numerator = self.numerator * other.denominator + other.numerator * self.denominator
            denominator = self.denominator * other.denominator
        elif isinstance(other, Integer):
            numerator = self.numerator + other.value * self.denominator
            denominator = self.denominator
        else:
            raise TypeError(f'Addition between {type(self)} and {type(other)} is not supported')
        return Rational(numerator, denominator)

    @Function.from_native
    def reverse_operator_plus(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the reverse addition operator"""
        return self.operator_plus.call(self, other)

    @Function.from_native
    def operator_minus(self, other: 'Integer | Rational') -> 'Rational':
        """Override the subtraction operator for integers"""
        if isinstance(other, Rational):
            numerator = self.numerator * other.denominator - other.numerator * self.denominator
            denominator = self.denominator * other.denominator
        elif isinstance(other, Integer):
            numerator = self.numerator - other.value * self.denominator
            denominator = self.denominator
        else:
            raise TypeError(f'Subtraction between {type(self)} and {type(other)} is not supported')
        return Rational(numerator, denominator)

    @Function.from_native
    def reverse_operator_minus(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the reverse addition operator"""
        return self.operator_plus.call(self.unary_operator_minus.call(self), other)

    @Function.from_native
    def operator_star(self, other: 'Integer | Rational') -> 'Rational':
        """Override the subtraction operator for integers"""
        if isinstance(other, Integer):
            other = Rational(other.value, 1)
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)

    @Function.from_native
    def reverse_operator_star(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the reverse multiplication operator"""
        return self.operator_star.call(self, other)

    @Function.from_native
    def operator_slash(self, other: 'Integer | Rational') -> 'Rational':
        """Override the subtraction operator for integers"""
        if isinstance(other, Integer):
            other = Rational(other.value, 1)
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)

    @Function.from_native
    def reverse_operator_slash(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the reverse division operator"""
        return self.operator_star.call(self.reciprocal.call(self), other)

    @Function.from_native
    def unary_operator_plus(self) -> 'Rational':
        """Implement unary plus for rational numbers"""
        return Rational(self.numerator, self.denominator)

    @Function.from_native
    def unary_operator_minus(self) -> 'Rational':
        """Implement unary minus for rational numbers"""
        return Rational(-self.numerator, self.denominator)

    @Function.from_native
    def reciprocal(self) -> 'Rational':
        """Calculate the reciprocal of the number"""
        return Rational(self.denominator, self.numerator)


class Integer(Value):
    """Represents an integer"""

    def __init__(self, value: int | str):
        self.leading_zeros = 0
        if isinstance(value, str):
            for c in value:
                if c != '0':
                    break
                self.leading_zeros += 1
        self.value = int(value)

    def __repr__(self) -> str:
        return str(self.value)

    @Function.from_native
    def operator_plus(self, other: 'Integer') -> 'Integer':
        """Override the addition operator for integers"""
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        return NotImplemented

    @Function.from_native
    def operator_minus(self, other: 'Integer') -> 'Integer':
        """Override the subtraction operator for integers"""
        if isinstance(other, Integer):
            return Integer(self.value - other.value)
        return NotImplemented

    @Function.from_native
    def operator_star(self, other: 'Integer') -> 'Integer':
        """Override the subtraction operator for integers"""
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        return NotImplemented

    @Function.from_native
    def operator_slash(self, other: 'Integer') -> 'Rational':
        """Override the subtraction operator for integers"""
        if isinstance(other, Integer):
            return Rational(self.value, other.value)
        return NotImplemented

    @Function.from_native
    def operator_dot(self, other: 'Integer') -> Rational:
        """Override the dot operator for integers"""
        x = len(str(other)) + other.leading_zeros
        return Rational(self.value * (10 ** x) + other.value, 10 ** x)


Frame = dict[str, Value]


class Context:
    """Represents the evaluation context of the program"""

    def __init__(self) -> None:
        self.stack: list[Frame] = []
        self.__returns: Optional[Value] = None
