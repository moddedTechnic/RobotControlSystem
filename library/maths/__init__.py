"""Items relating to maths"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['gcd']


def gcd(a: int, b: int) -> int:
    """Find the greatest common divisor of a and b."""
    x, y = abs(a), abs(b)
    if x == 0:
        return y
    if y == 0:
        return x
    if a < 0 and b < 0:
        return gcd(y, x % y) * -1
    return gcd(y, x % y)
