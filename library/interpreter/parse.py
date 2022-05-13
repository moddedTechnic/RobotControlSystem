"""The parser for the custom programming language"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['parse']

from typing import Iterable

from dependencies.sly.sly import Parser as _Parser

from .lex import Lexer, Token
from .variables import Integer


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
        ('left', PLUS, MINUS),
        ('left', STAR, SLASH),
        ('right', UMINUS, UPLUS),
        ('left', PERIOD),
    )

    def __init__(self):
        self.names = {}

    @_('IDENTIFIER IDENTIFIER ASSIGN expr SEMI')
    def statement(self, p):
        """Declare a variable"""
        typ = p.IDENTIFIER0
        name = p.IDENTIFIER1
        value = p.expr
        print(typ, name, value)

    @_('IDENTIFIER ASSIGN expr SEMI')
    def statement(self, p):
        name = p.IDENTIFIER
        value = p.expr

    @_('expr SEMI')
    def statement(self, p):
        return p.expr

    @_('expr PERIOD expr')
    def expr(self, p):
        """Dot expressions"""
        return p.expr0.operator_dot.call(p.expr0, p.expr1)

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

    @_('PLUS expr %prec UPLUS')
    def expr(self, p):
        """Unary plus expressions"""
        return _do_unary_operator('plus', '+', p.expr)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        """Unary minus expressions"""
        return _do_unary_operator('minus', '-', p.expr)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        """Bracketed expressions"""
        return p.expr

    @_('IDENTIFIER')
    def expr(self, p):
        """An expression containing a single identifier"""
        value: str = p.IDENTIFIER
        if value.isdigit():
            return Integer(p.IDENTIFIER)
        try:
            return self.names[p.IDENTIFIER]
        except LookupError:
            print(f'Undefined name {p.IDENTIFIER!r}')
            return 0


_parser = Parser()


def parse(tokens: Iterable[Token]):
    """Convert a stream of tokens to an abstract syntax tree"""
    return _parser.parse(tokens)
