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

    def __init__(self) -> None:
        self.context = Context()

    @_('statement')
    def program(self, p):
        """A program made of a single statement"""
        return [p.statement]

    @_('program statement')
    def program(self, p):
        """A program made of more than one statement"""
        return p.program + [p.statement]

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

    @_('KWD_CONST IDENTIFIER IDENTIFIER SEMI')
    def statement(self, p):
        """Declare a variable"""
        typ = self.context[p.IDENTIFIER0]
        if not (isinstance(typ, Type) or (isinstance(typ, type) and issubclass(typ, Value))):
            raise TypeError(f'Cannot create a variable of type "{typ}" - it is not a type')
        self.context.declare(p.IDENTIFIER1, typ, const=True)

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

    @_('expr SEMI')
    def statement(self, p):
        """A statement which is just an expression"""
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
