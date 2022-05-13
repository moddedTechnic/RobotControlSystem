"""Tests to ensure the interpreter works"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = []

import os
import sys
from pathlib import Path

__directory__ = Path(__file__).parent
sys.path.insert(0, os.fspath(__directory__))
sys.path.insert(1, os.fspath(__directory__.parent))

import unittest

from library.interpreter import evaluate


class ArithmeticTestCase(unittest.TestCase):
    def test_integer(self) -> None:
        self.assertEqual(evaluate('0;').value, 0)
        self.assertEqual(evaluate('1;').value, 1)
        self.assertEqual(evaluate('2;').value, 2)
        self.assertEqual(evaluate('3;').value, 3)
        self.assertEqual(evaluate('4;').value, 4)
        self.assertEqual(evaluate('5;').value, 5)
        self.assertEqual(evaluate('6;').value, 6)
        self.assertEqual(evaluate('7;').value, 7)
        self.assertEqual(evaluate('8;').value, 8)
        self.assertEqual(evaluate('9;').value, 9)

        self.assertEqual(evaluate('10;').value, 10)
        self.assertEqual(evaluate('11;').value, 11)
        self.assertEqual(evaluate('12;').value, 12)
        self.assertEqual(evaluate('13;').value, 13)
        self.assertEqual(evaluate('14;').value, 14)
        self.assertEqual(evaluate('15;').value, 15)
        self.assertEqual(evaluate('16;').value, 16)
        self.assertEqual(evaluate('17;').value, 17)
        self.assertEqual(evaluate('18;').value, 18)
        self.assertEqual(evaluate('19;').value, 19)

    def test_decimal(self) -> None:
        self.assertEqual((1, 10), evaluate('0.1;').as_tuple())
        self.assertEqual((1, 5),  evaluate('0.2;').as_tuple())
        self.assertEqual((3, 10), evaluate('0.3;').as_tuple())
        self.assertEqual((2, 5),  evaluate('0.4;').as_tuple())
        self.assertEqual((1, 2),  evaluate('0.5;').as_tuple())
        self.assertEqual((3, 5),  evaluate('0.6;').as_tuple())
        self.assertEqual((7, 10), evaluate('0.7;').as_tuple())
        self.assertEqual((4, 5),  evaluate('0.8;').as_tuple())
        self.assertEqual((9, 10), evaluate('0.9;').as_tuple())

        self.assertEqual((1, 100), evaluate('0.01;').as_tuple())
        self.assertEqual((1, 50),  evaluate('0.02;').as_tuple())
        self.assertEqual((3, 100), evaluate('0.03;').as_tuple())
        self.assertEqual((1, 25),  evaluate('0.04;').as_tuple())
        self.assertEqual((1, 20),  evaluate('0.05;').as_tuple())
        self.assertEqual((3, 50),  evaluate('0.06;').as_tuple())
        self.assertEqual((7, 100), evaluate('0.07;').as_tuple())
        self.assertEqual((2, 25),  evaluate('0.08;').as_tuple())
        self.assertEqual((9, 100), evaluate('0.09;').as_tuple())

    def test_rationals(self) -> None:
        self.assertEqual((3,  2), evaluate('1.5;').as_tuple())
        self.assertEqual((5,  2), evaluate('2.5;').as_tuple())
        self.assertEqual((15, 4), evaluate('3.75;').as_tuple())
        self.assertEqual((2107, 20), evaluate('105.35;').as_tuple())

    def test_addition(self) -> None:
        self.assertEqual(3, evaluate('1 + 2;').value)
        self.assertEqual((3, 1), evaluate('1.0 + 2.0;').as_tuple())
        self.assertEqual((3, 1), evaluate('1 + 2.0;').as_tuple())
        self.assertEqual((3, 1), evaluate('1.0 + 2;').as_tuple())

        self.assertEqual(1, evaluate('1 + 0;').value)
        self.assertEqual((1, 1), evaluate('1.0 + 0.0;').as_tuple())
        self.assertEqual((1, 1), evaluate('1 + 0.0;').as_tuple())
        self.assertEqual((1, 1), evaluate('1.0 + 0;').as_tuple())

        self.assertEqual((3, 10), evaluate('0.1 + 0.2;').as_tuple())
        self.assertEqual((33, 10), evaluate('1.1 + 2.2;').as_tuple())

    def test_subtraction(self) -> None:
        self.assertEqual(1, evaluate('2 - 1;').value)
        self.assertEqual((1, 1), evaluate('2.0 - 1.0;').as_tuple())
        self.assertEqual((1, 1), evaluate('2 - 1.0;').as_tuple())
        self.assertEqual((1, 1), evaluate('2.0 - 1;').as_tuple())

        self.assertEqual(2, evaluate('2 - 0;').value)
        self.assertEqual((2, 1), evaluate('2.0 - 0.0;').as_tuple())
        self.assertEqual((2, 1), evaluate('2 - 0.0;').as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 - 0;').as_tuple())

        self.assertEqual(-2, evaluate('0 - 2;').value)
        self.assertEqual((-2, 1), evaluate('0.0 - 2.0;').as_tuple())
        self.assertEqual((-2, 1), evaluate('0 - 2.0;').as_tuple())
        self.assertEqual((-2, 1), evaluate('0.0 - 2;').as_tuple())

    def test_multiplication(self) -> None:
        self.assertEqual(6, evaluate('2 * 3;').value)
        self.assertEqual((6, 1), evaluate('2.0 * 3.0;').as_tuple())
        self.assertEqual((6, 1), evaluate('2 * 3.0;').as_tuple())
        self.assertEqual((6, 1), evaluate('2.0 * 3;').as_tuple())

        self.assertEqual(0, evaluate('2 * 0;').value)
        self.assertEqual((0, 1), evaluate('2.0 * 0.0;').as_tuple())
        self.assertEqual((0, 1), evaluate('2 * 0.0;').as_tuple())
        self.assertEqual((0, 1), evaluate('2.0 * 0;').as_tuple())

        self.assertEqual(2, evaluate('2 * 1;').value)
        self.assertEqual((2, 1), evaluate('2.0 * 1.0;').as_tuple())
        self.assertEqual((2, 1), evaluate('2 * 1.0;').as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 * 1;').as_tuple())

    def test_division(self) -> None:
        self.assertEqual((2, 3), evaluate('2 / 3;').as_tuple())
        self.assertEqual((2, 3), evaluate('2.0 / 3.0;').as_tuple())
        self.assertEqual((2, 3), evaluate('2 / 3.0;').as_tuple())
        self.assertEqual((2, 3), evaluate('2.0 / 3;').as_tuple())

        with self.assertRaises(ZeroDivisionError):
            evaluate('2 / 0;')
        with self.assertRaises(ZeroDivisionError):
            evaluate('2.0 / 0.0;')
        with self.assertRaises(ZeroDivisionError):
            evaluate('2 / 0.0;')
        with self.assertRaises(ZeroDivisionError):
            evaluate('2.0 / 0;')

        self.assertEqual((2, 1), evaluate('2 / 1;').as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 / 1.0;').as_tuple())
        self.assertEqual((2, 1), evaluate('2 / 1.0;').as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 / 1;').as_tuple())


if __name__ == '__main__':
    unittest.main()
