"""Items relating to the interpreter of the custom programming language"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['evaluate']


from .lex import tokenize
from .parse import parse


def evaluate(code: str):
    """Evaluate a code string"""
    return parse(tokenize(code))
