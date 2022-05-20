"""Items relating to the interpreter of the custom programming language"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['evaluate']

from typing import Optional

from .lex import tokenize, Lexer
from .parse import parse, Parser, default_parser


def evaluate(code: str, *, lexer: Optional[Lexer] = None, parser: Optional[Parser] = None):
    """Evaluate a code string"""
    t = tokenize if lexer is None else lexer.tokenize
    if parser is None:
        parser = default_parser
    return parser.parse(t(code)).evaluate(parser.context)
