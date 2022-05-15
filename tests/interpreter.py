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
from library.interpreter.parse import Parser
from library.interpreter.variables import Integer, Type, Variable, undefined, Rational, Boolean, Undefined, Null, null


class ArithmeticTestCase(unittest.TestCase):
    def test_integer(self) -> None:
        self.assertEqual(evaluate('0;')[0].value, 0)
        self.assertEqual(evaluate('1;')[0].value, 1)
        self.assertEqual(evaluate('2;')[0].value, 2)
        self.assertEqual(evaluate('3;')[0].value, 3)
        self.assertEqual(evaluate('4;')[0].value, 4)
        self.assertEqual(evaluate('5;')[0].value, 5)
        self.assertEqual(evaluate('6;')[0].value, 6)
        self.assertEqual(evaluate('7;')[0].value, 7)
        self.assertEqual(evaluate('8;')[0].value, 8)
        self.assertEqual(evaluate('9;')[0].value, 9)

        self.assertEqual(evaluate('10;')[0].value, 10)
        self.assertEqual(evaluate('11;')[0].value, 11)
        self.assertEqual(evaluate('12;')[0].value, 12)
        self.assertEqual(evaluate('13;')[0].value, 13)
        self.assertEqual(evaluate('14;')[0].value, 14)
        self.assertEqual(evaluate('15;')[0].value, 15)
        self.assertEqual(evaluate('16;')[0].value, 16)
        self.assertEqual(evaluate('17;')[0].value, 17)
        self.assertEqual(evaluate('18;')[0].value, 18)
        self.assertEqual(evaluate('19;')[0].value, 19)

    def test_decimal(self) -> None:
        self.assertEqual((1, 10), evaluate('0.1;')[0].as_tuple())
        self.assertEqual((1, 5),  evaluate('0.2;')[0].as_tuple())
        self.assertEqual((3, 10), evaluate('0.3;')[0].as_tuple())
        self.assertEqual((2, 5),  evaluate('0.4;')[0].as_tuple())
        self.assertEqual((1, 2),  evaluate('0.5;')[0].as_tuple())
        self.assertEqual((3, 5),  evaluate('0.6;')[0].as_tuple())
        self.assertEqual((7, 10), evaluate('0.7;')[0].as_tuple())
        self.assertEqual((4, 5),  evaluate('0.8;')[0].as_tuple())
        self.assertEqual((9, 10), evaluate('0.9;')[0].as_tuple())

        self.assertEqual((1, 100), evaluate('0.01;')[0].as_tuple())
        self.assertEqual((1, 50),  evaluate('0.02;')[0].as_tuple())
        self.assertEqual((3, 100), evaluate('0.03;')[0].as_tuple())
        self.assertEqual((1, 25),  evaluate('0.04;')[0].as_tuple())
        self.assertEqual((1, 20),  evaluate('0.05;')[0].as_tuple())
        self.assertEqual((3, 50),  evaluate('0.06;')[0].as_tuple())
        self.assertEqual((7, 100), evaluate('0.07;')[0].as_tuple())
        self.assertEqual((2, 25),  evaluate('0.08;')[0].as_tuple())
        self.assertEqual((9, 100), evaluate('0.09;')[0].as_tuple())

    def test_rationals(self) -> None:
        self.assertEqual((3,  2), evaluate('1.5;')[0].as_tuple())
        self.assertEqual((5,  2), evaluate('2.5;')[0].as_tuple())
        self.assertEqual((15, 4), evaluate('3.75;')[0].as_tuple())
        self.assertEqual((2107, 20), evaluate('105.35;')[0].as_tuple())

    def test_addition(self) -> None:
        self.assertEqual(3, evaluate('1 + 2;')[0].value)
        self.assertEqual((3, 1), evaluate('1.0 + 2.0;')[0].as_tuple())
        self.assertEqual((3, 1), evaluate('1 + 2.0;')[0].as_tuple())
        self.assertEqual((3, 1), evaluate('1.0 + 2;')[0].as_tuple())

        self.assertEqual(1, evaluate('1 + 0;')[0].value)
        self.assertEqual((1, 1), evaluate('1.0 + 0.0;')[0].as_tuple())
        self.assertEqual((1, 1), evaluate('1 + 0.0;')[0].as_tuple())
        self.assertEqual((1, 1), evaluate('1.0 + 0;')[0].as_tuple())

        self.assertEqual((3, 10), evaluate('0.1 + 0.2;')[0].as_tuple())
        self.assertEqual((33, 10), evaluate('1.1 + 2.2;')[0].as_tuple())

    def test_subtraction(self) -> None:
        self.assertEqual(1, evaluate('2 - 1;')[0].value)
        self.assertEqual((1, 1), evaluate('2.0 - 1.0;')[0].as_tuple())
        self.assertEqual((1, 1), evaluate('2 - 1.0;')[0].as_tuple())
        self.assertEqual((1, 1), evaluate('2.0 - 1;')[0].as_tuple())

        self.assertEqual(2, evaluate('2 - 0;')[0].value)
        self.assertEqual((2, 1), evaluate('2.0 - 0.0;')[0].as_tuple())
        self.assertEqual((2, 1), evaluate('2 - 0.0;')[0].as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 - 0;')[0].as_tuple())

        self.assertEqual(-2, evaluate('0 - 2;')[0].value)
        self.assertEqual((-2, 1), evaluate('0.0 - 2.0;')[0].as_tuple())
        self.assertEqual((-2, 1), evaluate('0 - 2.0;')[0].as_tuple())
        self.assertEqual((-2, 1), evaluate('0.0 - 2;')[0].as_tuple())

    def test_multiplication(self) -> None:
        self.assertEqual(6, evaluate('2 * 3;')[0].value)
        self.assertEqual((6, 1), evaluate('2.0 * 3.0;')[0].as_tuple())
        self.assertEqual((6, 1), evaluate('2 * 3.0;')[0].as_tuple())
        self.assertEqual((6, 1), evaluate('2.0 * 3;')[0].as_tuple())

        self.assertEqual(0, evaluate('2 * 0;')[0].value)
        self.assertEqual((0, 1), evaluate('2.0 * 0.0;')[0].as_tuple())
        self.assertEqual((0, 1), evaluate('2 * 0.0;')[0].as_tuple())
        self.assertEqual((0, 1), evaluate('2.0 * 0;')[0].as_tuple())

        self.assertEqual(2, evaluate('2 * 1;')[0].value)
        self.assertEqual((2, 1), evaluate('2.0 * 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), evaluate('2 * 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 * 1;')[0].as_tuple())

    def test_division(self) -> None:
        self.assertEqual((2, 3), evaluate('2 / 3;')[0].as_tuple())
        self.assertEqual((2, 3), evaluate('2.0 / 3.0;')[0].as_tuple())
        self.assertEqual((2, 3), evaluate('2 / 3.0;')[0].as_tuple())
        self.assertEqual((2, 3), evaluate('2.0 / 3;')[0].as_tuple())

        with self.assertRaises(ZeroDivisionError):
            evaluate('2 / 0;')
        with self.assertRaises(ZeroDivisionError):
            evaluate('2.0 / 0.0;')
        with self.assertRaises(ZeroDivisionError):
            evaluate('2 / 0.0;')
        with self.assertRaises(ZeroDivisionError):
            evaluate('2.0 / 0;')

        self.assertEqual((2, 1), evaluate('2 / 1;')[0].as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 / 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), evaluate('2 / 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), evaluate('2.0 / 1;')[0].as_tuple())

    def test_variable_declaration(self) -> None:
        parser = Parser()
        parser.context.push({'int': Variable(Integer, Type, True)})

        with parser.context:
            evaluate('int x;', parser=parser)
            self.assertIn('x', parser.context)
            self.assertIs(parser.context['x'], undefined)

        with parser.context:
            evaluate('int y = 5;', parser=parser)
            self.assertIn('y', parser.context)
            self.assertIsInstance(parser.context['y'], Integer)
            self.assertEqual(parser.context['y'].value, 5)

    def test_variable_definition(self) -> None:
        parser = Parser()
        parser.context.push({'int': Variable(Integer, Type, True)})

        with parser.context:
            evaluate('int x;', parser=parser)
            evaluate('x = 5;', parser=parser)
            self.assertIn('x', parser.context)
            self.assertIsInstance(parser.context['x'], Integer)
            self.assertEqual(5, parser.context['x'].value)

    def test_variable_access(self) -> None:
        parser = Parser()
        parser.context.push({'int': Variable(Integer, Type, True)})

        with parser.context:
            evaluate('int x = 5;', parser=parser)
            x = evaluate('x;', parser=parser)[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(5, x.value)

        with parser.context:
            with self.assertRaises(NameError):
                evaluate('y;', parser=parser)

    def test_boolean_variables(self) -> None:
        parser = Parser()
        parser.context.push({
            'bool': Variable(Boolean, Type, True),
        })

        with parser.context:
            true = evaluate('true;', parser=parser)[0]
            self.assertIsInstance(true, Boolean)
            self.assertIs(true.value, True)

        with parser.context:
            false = evaluate('false;', parser=parser)[0]
            self.assertIsInstance(false, Boolean)
            self.assertIs(false.value, False)

    def test_nullish_variables(self) -> None:
        _undefined = evaluate('undefined;')[0]
        self.assertIsInstance(_undefined, Undefined)
        self.assertIs(_undefined, undefined)

        _null = evaluate('null;')[0]
        self.assertIsInstance(_null, Null)
        self.assertIs(_null, null)

    def test_auto_variables(self) -> None:
        parser = Parser()

        with parser.context:
            evaluate('auto x = 5;', parser=parser)
            x = evaluate('x;', parser=parser)[0]
            self.assertIs(parser.context.get_variable('x').type, Integer)
            self.assertIsInstance(x, Integer)
            self.assertEqual(x.value, 5)

        with parser.context:
            evaluate('auto pi = 22 / 7;', parser=parser)
            pi = evaluate('pi;', parser=parser)[0]
            self.assertIs(parser.context.get_variable('pi').type, Rational)
            self.assertIsInstance(pi, Rational)
            self.assertEqual((22, 7), pi.as_tuple())

    def test_weird_variables(self) -> None:
        parser = Parser()
        parser.context.push({
            'int': Variable(Integer, Type, True),
            'rational': Variable(Rational, Type, True)
        })

        with parser.context:
            evaluate('int 0 = 1;', parser=parser)
            _0 = evaluate('0;', parser=parser)[0]
            self.assertIsInstance(_0, Integer)
            self.assertEqual(1, _0.value)

        with parser.context:
            evaluate('int three = 3;', parser=parser)
            evaluate('rational pi = three.14;', parser=parser)
            pi = evaluate('pi;', parser=parser)[0]
            self.assertIsInstance(pi, Rational)
            self.assertEqual((157, 50), pi.as_tuple())

    def test_increment(self) -> None:
        parser = Parser()

        with parser.context:
            evaluate('auto x = 0;', parser=parser)
            x = evaluate('x++;', parser=parser)[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(1, x.value)
            x = evaluate('x++;', parser=parser)[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(2, x.value)

        with parser.context:
            evaluate('auto y = 0.0;', parser=parser)
            y = evaluate('y++;', parser=parser)[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((1, 1), y.as_tuple())
            y = evaluate('y++;', parser=parser)[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((2, 1), y.as_tuple())

    def test_decrement(self) -> None:
        parser = Parser()

        with parser.context:
            evaluate('auto x = 0;', parser=parser)
            x = evaluate('x--;', parser=parser)[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(-1, x.value)
            x = evaluate('x--;', parser=parser)[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(-2, x.value)

        with parser.context:
            evaluate('auto y = 0.0;', parser=parser)
            y = evaluate('y--;', parser=parser)[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((-1, 1), y.as_tuple())
            y = evaluate('y--;', parser=parser)[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((-2, 1), y.as_tuple())


if __name__ == '__main__':
    unittest.main()
