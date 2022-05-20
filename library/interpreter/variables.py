"""Items relating to the storage of variables and functions"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = [
    'Integer', 'Rational', 'Context',
    'Type', 'Value', 'Variable', 'Boolean',
    'Undefined', 'Null',
    'null', 'undefined', 'false', 'true',
]

from dataclasses import dataclass
from typing import Any, Union, Optional, Callable, Type as PyType

from library import maths


@dataclass
class Value:
    """Represents a value"""
    typ: Union[type, 'Type']
    value: Any


class Type(Value):
    """Represents a type"""

    def __init__(self, value: Any) -> None:
        super().__init__(Type, value)


class Undefined(Value):
    """Used to mark that a name has no value"""

    def __init__(self) -> None:
        super().__init__(type(self), None)

    def __repr__(self) -> str:
        return f'undefined'


class Null(Value):
    """Used to mark that a name has no value"""

    def __init__(self) -> None:
        super().__init__(type(self), None)

    def __repr__(self) -> str:
        return f'null'


undefined = Undefined()
null = Null()


class Signature:
    """Represents a function signature"""


class Arguments:
    """Represents a collection of arguments passed to a function"""


class Function(Value):
    """Represents a function in the context"""

    def __init__(self, signature: Signature, body: list | Callable):
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
        super().__init__(type(self), None)
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
    def unary_operator_increment(self) -> 'Rational':
        """Implement the `++` operator"""
        return Rational(self.numerator + self.denominator, self.denominator)

    @Function.from_native
    def unary_operator_decrement(self) -> 'Rational':
        """Implement the `--` operator"""
        return Rational(self.numerator - self.denominator, self.denominator)

    @Function.from_native
    def unary_operator_plus(self) -> 'Rational':
        """Implement unary plus for rational numbers"""
        return Rational(self.numerator, self.denominator)

    @Function.from_native
    def unary_operator_minus(self) -> 'Rational':
        """Implement unary minus for rational numbers"""
        return Rational(-self.numerator, self.denominator)

    @Function.from_native
    def assignment_operator_plus(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the `+=` operator"""
        return self.operator_plus.call(self, other)

    @Function.from_native
    def assignment_operator_minus(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the `-=` operator"""
        return self.operator_minus.call(self, other)

    @Function.from_native
    def assignment_operator_star(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the `*=` operator"""
        return self.operator_star.call(self, other)

    @Function.from_native
    def assignment_operator_slash(self, other: 'Integer | Rational') -> 'Rational':
        """Implement the `/=` operator"""
        return self.operator_slash.call(self, other)

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
        super().__init__(type(self), int(value))

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
    def operator_get(self, other: 'Integer | str') -> Rational:
        """Override the dot operator for integers"""
        if isinstance(other, str):
            x = len(other)
            for c in other:
                if c != '0':
                    break
                x += 1
            if other.startswith('0'):
                x -= 1
            value = int(other)
        else:
            x = len(str(other)) + other.leading_zeros
            value = other.value
        return Rational(self.value * (10 ** x) + value, 10 ** x)

    @Function.from_native
    def operator_less(self, other: 'Integer') -> 'Boolean':
        """Implement the `<` operator"""
        return Boolean(self.value < other.value)

    @Function.from_native
    def operator_less_equal(self, other: 'Integer') -> 'Boolean':
        """Implement the `<=` operator"""
        return Boolean(self.value <= other.value)

    @Function.from_native
    def operator_greater(self, other: 'Integer') -> 'Boolean':
        """Implement the `>` operator"""
        return Boolean(self.value > other.value)

    @Function.from_native
    def operator_greater_equal(self, other: 'Integer') -> 'Boolean':
        """Implement the `>=` operator"""
        return Boolean(self.value >= other.value)

    @Function.from_native
    def operator_equality(self, other: 'Integer') -> 'Boolean':
        """Implement the `==` operator"""
        return Boolean(self.value == other.value)

    @Function.from_native
    def operator_nonequality(self, other: 'Integer') -> 'Boolean':
        """Implement the `!=` operator"""
        return Boolean(self.value != other.value)

    @Function.from_native
    def unary_operator_increment(self) -> 'Integer':
        """Implement the `++` operator"""
        return Integer(self.value + 1)

    @Function.from_native
    def unary_operator_decrement(self) -> 'Integer':
        """Implement the `--` operator"""
        return Integer(self.value - 1)

    @Function.from_native
    def assignment_operator_plus(self, other: 'Integer | Rational') -> 'Integer':
        """Implement the `+=` operator"""
        return Integer(self.value + other.value)

    @Function.from_native
    def assignment_operator_minus(self, other: 'Integer | Rational') -> 'Integer':
        """Implement the `-=` operator"""
        return Integer(self.value - other.value)

    @Function.from_native
    def assignment_operator_star(self, other: 'Integer | Rational') -> 'Integer':
        """Implement the `*=` operator"""
        return Integer(self.value * other.value)

    @Function.from_native
    def assignment_operator_slash(self, other: 'Integer | Rational') -> 'Integer':
        """Implement the `/=` operator"""
        return Integer(self.value / other.value)


class Boolean(Value):
    """Represents a boolean value"""

    def __init__(self, value: bool):
        super().__init__(type(self), value)

    def __eq__(self, other: 'Boolean') -> bool:
        return self.value is other.value


true = Boolean(True)
false = Boolean(False)


@dataclass
class Variable:
    """Represents a variable in the context"""
    value: Value | PyType[Value]
    type: type
    const: bool = False


Frame = dict[str, Variable]


class Context:
    """Represents the evaluation context of the program"""

    def __init__(self) -> None:
        self.stack: list[Frame] = []
        self.__returns: Optional[Value] = None

    def __getitem__(self, name: str) -> Value:
        return self.get_variable(name).value

    def __setitem__(self, name: str, value: Value) -> None:
        for frame in reversed(self.stack):
            if name in frame and isinstance(value, frame[name].type) and not frame[name].const:
                frame[name].value = value
                return
        raise NameError(f'"{name}" was not declared in the current scope, or it was declared as constant')

    def __contains__(self, name: str) -> bool:
        for frame in self.stack:
            if name in frame:
                return True
        return False

    def __enter__(self) -> None:
        self.push()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.pop()

    def declare(self, name: str, typ: type | Type, value: Value = undefined, const: bool = False) -> None:
        """Declare a variable in the top-most stack frame"""
        self.stack[-1][name] = Variable(value, typ, const)

    def push(self, frame: Optional[Frame] = None) -> None:
        """Push a frame to the stack"""
        self.stack.append({} if frame is None else frame)

    def pop(self) -> None:
        """Pop a frame from the stack"""
        self.stack.pop()

    def get_variable(self, name: str) -> Variable:
        """Get the raw variable for the given name"""
        for frame in reversed(self.stack):
            if name in frame and frame[name] is not undefined:
                return frame[name]
        raise NameError(f'"{name}" was not defined')
