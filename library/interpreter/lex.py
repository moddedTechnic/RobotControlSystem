"""The lexer for the custom programming language"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Lexer', 'Token', 'tokenize']

from typing import Iterable

from dependencies.sly.sly import Lexer as _Lexer
# noinspection PyProtectedMember
from dependencies.sly.sly.lex import Token

from library.functions import unused


# noinspection PyUnboundLocalVariable,PyRedeclaration
class Lexer(_Lexer):
    """The lexer to convert a code string to a sequence of tokens"""

    tokens = {
        IDENTIFIER,
        PLUS, MINUS, STAR, SLASH, PERIOD,
        EQUALS,
        LPAREN, RPAREN,
        SEMI,
        KWD_FOR, KWD_WHILE, KWD_IF,
        KWD_CLASS,
        KWD_AUTO, KWD_CONST, KWD_FINAL,
        KWD_NONLOCAL,
    }

    ignore = ' \t'
    ignore_newline = r'\n+'
    ignore_comment_line = r'//.*\n'
    ignore_comment_multi = r'/\*.*\*/'

    KWD_FOR = r'for'
    KWD_WHILE = r'while'
    KWD_IF = r'if'
    KWD_CLASS = f'class'
    KWD_AUTO = r'auto'
    KWD_CONST = r'const'
    KWD_FINAL = r'final'
    KWD_NONLOCAL = r'nonlocal'

    IDENTIFIER = r'[a-zA-Z0-9_]+'

    PLUS = r'\+'
    MINUS = r'-'
    STAR = r'\*'
    SLASH = r'/'
    EQUALS = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    PERIOD = r'\.'
    SEMI = r';'

    def ignore_newline(self, t: Token) -> None:
        """Increment the line number for each new line encountered"""
        self.lineno += t.value.count('\n')

    def ignore_comment_line(self, t: Token) -> None:
        """Increment the line number as we ignore a single line comment"""
        unused(t)
        self.lineno += 1

    def ignore_comment_multi(self, t: Token) -> None:
        """Increment the line number for each newline in a multi-line comment"""
        self.lineno += t.value.count('\n')

    def error(self, t: Token):
        """When an error occurs, throw a syntax error"""
        raise SyntaxError(f'An unexpected sequence ("{t.value}") was encountered at line {t.lineno}, column {t.index}')


def tokenize(code: str) -> Iterable[Token]:
    """Convert a code string to a stream of tokens"""
    return Lexer().tokenize(code)
