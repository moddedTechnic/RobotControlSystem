"""The parser for the custom programming language"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['parse', 'Parser']

from typing import Iterable

from dependencies.sly.sly import Parser as _Parser

from .lex import Lexer, Token
from .variables import Integer, Context, Type, Value, undefined, false, true, null


def _do_binary_operator(name: str, op: str, a, b):
    handler_name = f'operator_{name}'
    if hasattr(a, handler_name):
        handler = getattr(a, handler_name)
        if (result := handler.call(a, b)) is not NotImplemented:
            return result
    reverse_handler_name = f'reverse_operator_{name}'
    if hasattr(b, reverse_handler_name):
        reverse_handler = getattr(b, reverse_handler_name)
        if (result := reverse_handler.call(b, a)) is not NotImplemented:
            return result
    raise TypeError(
        f'unsupported operand type(s) for {op}: "{type(a).__name__}" and "{type(b).__name__}"'
    )


def _do_comparison_operator(name: str, back_name: str, op: str, a, b):
    handler_name = f'operator_{name}'
    if hasattr(a, handler_name):
        handler = getattr(a, handler_name)
        if (result := handler.call(a, b)) is not NotImplemented:
            return result
    back_handler_name = f'operator_{back_name}'
    if hasattr(b, back_handler_name):
        back_handler = getattr(b, back_handler_name)
        if (result := back_handler.call(b, a)) is not NotImplemented:
            return result
    raise TypeError(
        f'unsupported operand type(s) for {op}: "{type(a).__name__}" and "{type(b).__name__}"'
    )


def _do_assignment_operator(name: str, op: str, a, b):
    handler_name = f'assignment_operator_{name}'
    if hasattr(a, handler_name):
        handler = getattr(a, handler_name)
        if (result := handler.call(a, b)) is not NotImplemented:
            return result
    raise TypeError(
        f'unsupported operand type(s) for {op}=: "{type(a).__name__}" and "{type(b).__name__}"'
    )


def _do_unary_operator(name: str, op: str, a):
    handler_name = f'unary_operator_{name}'
    if hasattr(a, handler_name):
        handler = getattr(a, handler_name)
        if (result := handler.call(a)) is not NotImplemented:
            return result
    raise TypeError(
        f'bad operand type for {op}: "{type(a).__name__}"'
    )


class Parser(_Parser):
    """The parser to parse and evaluate code"""

    tokens = Lexer.tokens

    precedence = (
        ('left', LESS, LESS_EQUAL, GREATER, GREATER_EQUAL, EQUALITY, NONEQUALITY, IDENTITY),
        ('left', PLUS, MINUS),
        ('left', STAR, SLASH),
        ('right', UNARY_MINUS, UNARY_PLUS),
        ('right', INCREMENT, DECREMENT),
        ('left', PERIOD),
    )

    def __init__(self) -> None:
        self.context = Context()

    @_('statement')
    def program(self, p):
        """A program made of a single statement"""
        return p.statement,

    @_('program statement')
    def program(self, p):
        """A program made of more than one statement"""
        return *p.program, p.statement

    @_('IDENTIFIER IDENTIFIER EQUALS expr SEMI')
    def statement(self, p):
        """Declare a variable"""
        typ = self.context[p.IDENTIFIER0]
        if not (isinstance(typ, Type) or (isinstance(typ, type) and issubclass(typ, Value))):
            raise TypeError(f'Cannot create a variable of type "{typ}" - it is not a type')
        self.context.declare(p.IDENTIFIER1, typ, p.expr)

    @_('IDENTIFIER IDENTIFIER SEMI')
    def statement(self, p):
        """Declare a variable"""
        typ = self.context[p.IDENTIFIER0]
        if not (isinstance(typ, Type) or (isinstance(typ, type) and issubclass(typ, Value))):
            raise TypeError(f'Cannot create a variable of type "{typ}" - it is not a type')
        self.context.declare(p.IDENTIFIER1, typ)

    @_('KWD_CONST IDENTIFIER IDENTIFIER EQUALS expr SEMI')
    def statement(self, p):
        """Declare a variable"""
        typ = self.context[p.IDENTIFIER0]
        if not (isinstance(typ, Type) or (isinstance(typ, type) and issubclass(typ, Value))):
            raise TypeError(f'Cannot create a variable of type "{typ}" - it is not a type')
        self.context.declare(p.IDENTIFIER1, typ, p.expr, const=True)

    @_('KWD_AUTO IDENTIFIER EQUALS expr SEMI')
    def statement(self, p):
        """Declare a variable"""
        self.context.declare(p.IDENTIFIER, p.expr.typ, p.expr)

    @_('KWD_CONST KWD_AUTO IDENTIFIER EQUALS expr SEMI')
    def statement(self, p):
        """Declare a variable"""
        self.context.declare(p.IDENTIFIER, p.expr.typ, p.expr, const=True)

    @_('IDENTIFIER EQUALS expr SEMI')
    def statement(self, p):
        """Assign a value to a variable"""
        self.context[p.IDENTIFIER] = p.expr

    @_('operator_assign SEMI')
    def statement(self, p):
        """Assignment operators such as `+=`"""
        return p.operator_assign

    @_('expr SEMI')
    def statement(self, p):
        """A statement which is just an expression"""
        return p.expr

    @_('LEFT_BRACE program RIGHT_BRACE')
    def statement(self, p) -> list:
        """Represents a block of statements"""
        return p.program

    @_('IDENTIFIER PLUS_EQUALS expr')
    def operator_assign(self, p):
        """The `+=` operator"""
        self.context[p.IDENTIFIER] = _do_assignment_operator('plus', '+', self.context[p.IDENTIFIER], p.expr)

    @_('IDENTIFIER MINUS_EQUALS expr')
    def operator_assign(self, p):
        """The `-=` operator"""
        self.context[p.IDENTIFIER] = _do_assignment_operator('minus', '-', self.context[p.IDENTIFIER], p.expr)

    @_('IDENTIFIER STAR_EQUALS expr')
    def operator_assign(self, p):
        """The `*=` operator"""
        self.context[p.IDENTIFIER] = _do_assignment_operator('star', '*', self.context[p.IDENTIFIER], p.expr)

    @_('IDENTIFIER SLASH_EQUALS expr')
    def operator_assign(self, p):
        """The `/=` operator"""
        self.context[p.IDENTIFIER] = _do_assignment_operator('slash', '/', self.context[p.IDENTIFIER], p.expr)

    @_('expr PERIOD expr')
    def access_expr(self, p):
        """Dot expressions"""
        return p.expr0.operator_dot.call(p.expr0, p.expr1)

    @_('access_expr')
    def expr(self, p):
        """Dot expressions are expressions"""
        return p.access_expr

    @_('expr LESS expr')
    def logic_expr(self, p):
        """a < b"""
        return _do_comparison_operator('less', 'greater', '<', p.expr0, p.expr1)

    @_('expr LESS_EQUAL expr')
    def logic_expr(self, p):
        """a <= b"""
        return _do_comparison_operator('less_equal', 'greater_equal', '<=', p.expr0, p.expr1)

    @_('expr GREATER expr')
    def logic_expr(self, p):
        """a > b"""
        return _do_comparison_operator('greater', 'less', '>', p.expr0, p.expr1)

    @_('expr GREATER_EQUAL expr')
    def logic_expr(self, p):
        """a >= b"""
        return _do_comparison_operator('greater_equal', 'less_equal', '>=', p.expr0, p.expr1)

    @_('expr EQUALITY expr')
    def logic_expr(self, p):
        """a == b"""
        return _do_comparison_operator('equality', 'equality', '==', p.expr0, p.expr1)

    @_('expr NONEQUALITY expr')
    def logic_expr(self, p):
        """a != b"""
        return _do_comparison_operator('nonequality', 'nonequality', '!=', p.expr0, p.expr1)

    @_('expr IDENTITY expr')
    def logic_expr(self, p):
        """a is b"""
        return _do_comparison_operator('identity', 'identity', 'is', p.expr0, p.expr1)

    @_('logic_expr')
    def expr(self, p):
        """Dot expressions are expressions"""
        return p.logic_expr

    @_('expr PLUS expr')
    def expr(self, p):
        """Plus expressions"""
        return _do_binary_operator('plus', '+', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        """Minus expressions"""
        return _do_binary_operator('minus', '+', p.expr0, p.expr1)

    @_('expr STAR expr')
    def expr(self, p):
        """Star expressions"""
        return _do_binary_operator('star', '*', p.expr0, p.expr1)

    @_('expr SLASH expr')
    def expr(self, p):
        """Slash expressions"""
        return _do_binary_operator('slash', '/', p.expr0, p.expr1)

    @_('IDENTIFIER INCREMENT')
    def expr(self, p):
        """Increment expressions"""
        name = p.IDENTIFIER
        self.context[name] = _do_unary_operator('increment', '++', self.context[name])
        return self.context[name]

    @_('IDENTIFIER DECREMENT')
    def expr(self, p):
        """Increment expressions"""
        name = p.IDENTIFIER
        self.context[name] = _do_unary_operator('decrement', '--', self.context[name])
        return self.context[name]

    @_('PLUS expr %prec UNARY_PLUS')
    def expr(self, p):
        """Unary plus expressions"""
        return _do_unary_operator('plus', '+', p.expr)

    @_('MINUS expr %prec UNARY_MINUS')
    def expr(self, p):
        """Unary minus expressions"""
        return _do_unary_operator('minus', '-', p.expr)

    @_('LEFT_PAREN expr RIGHT_PAREN')
    def expr(self, p):
        """Bracketed expressions"""
        return p.expr

    @_('IDENTIFIER')
    def expr(self, p):
        """An expression containing a single identifier"""
        name: str = p.IDENTIFIER
        try:
            return self.context[name]
        except NameError:
            if name.isdigit():
                return Integer(name)
            if name == 'true':
                return true
            if name == 'false':
                return false
            if name == 'null':
                return null
            if name == 'undefined':
                return undefined
            raise


_parser = Parser()


def parse(tokens: Iterable[Token]):
    """Convert a stream of tokens to an abstract syntax tree"""
    return _parser.parse(tokens)
