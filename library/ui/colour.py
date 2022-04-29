"""Stores colours"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = [
    'rgb',
    'WHITE', 'BLACK',
    'RED', 'GREEN', 'BLUE',
]


def rgb(code: str) -> tuple[int, int, int]:
    """Convert a hex code to a colour tuple"""
    colour_code = code[1:]
    if len(colour_code) == 6:
        r, g, b = colour_code[:2], colour_code[2:4], colour_code[4:]
    elif len(colour_code) == 3:
        r, g, b = colour_code[:1], colour_code[1:2], colour_code[2:]
        r *= 2
        g *= 2
        b *= 2
    elif len(colour_code) == 2:
        r = g = b = colour_code
    elif len(colour_code) == 1:
        r = g = b = colour_code * 2
    else:
        raise ValueError(f'Could not parse the colour code "{code}"')
    return int(r, 16), int(g, 16), int(b, 16)


WHITE = rgb('#f')
BLACK = rgb('#0')

RED = rgb('#f00')
GREEN = rgb('#0f0')
BLUE = rgb('#00f')
