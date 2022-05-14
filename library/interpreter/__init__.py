"""Items relating to the interpreter of the custom programming language"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['evaluate']

from typing import Optional

from .lex import tokenize, Lexer
from .parse import parse, Parser


def evaluate(code: str, *, lexer: Optional[Lexer] = None, parser: Optional[Parser] = None):
    """Evaluate a code string"""
    t = tokenize if lexer is None else lexer.tokenize
    p = parse if parser is None else parser.parse
    return p(t(code))
