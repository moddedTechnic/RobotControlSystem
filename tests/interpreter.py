"""Tests to ensure the interpreter works"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = []

import os
import sys
from functools import partial
from pathlib import Path

__directory__ = Path(__file__).parent
sys.path.insert(0, os.fspath(__directory__))
sys.path.insert(1, os.fspath(__directory__.parent))

import unittest

from library.interpreter import evaluate
from library.interpreter.parse import Parser
from library.interpreter.variables import (
    Variable,
    Type, Integer, Rational,
    Undefined, Null, Boolean,
    null, undefined, true, false,
)


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare for the test by creating a parser"""
        self.parser = Parser()
        self.parser.context.push({
            'int': Variable(Integer, Type, True),
            'rational': Variable(Rational, Type, True),
            'bool': Variable(Boolean, Type, True),
        })
        self.evaluate = partial(evaluate, parser=self.parser)


class NumbersTestCase(BaseTest):
    def test_integer(self) -> None:
        self.assertEqual(self.evaluate('0;')[0].value, 0)
        self.assertEqual(self.evaluate('1;')[0].value, 1)
        self.assertEqual(self.evaluate('2;')[0].value, 2)
        self.assertEqual(self.evaluate('3;')[0].value, 3)
        self.assertEqual(self.evaluate('4;')[0].value, 4)
        self.assertEqual(self.evaluate('5;')[0].value, 5)
        self.assertEqual(self.evaluate('6;')[0].value, 6)
        self.assertEqual(self.evaluate('7;')[0].value, 7)
        self.assertEqual(self.evaluate('8;')[0].value, 8)
        self.assertEqual(self.evaluate('9;')[0].value, 9)

        self.assertEqual(self.evaluate('10;')[0].value, 10)
        self.assertEqual(self.evaluate('11;')[0].value, 11)
        self.assertEqual(self.evaluate('12;')[0].value, 12)
        self.assertEqual(self.evaluate('13;')[0].value, 13)
        self.assertEqual(self.evaluate('14;')[0].value, 14)
        self.assertEqual(self.evaluate('15;')[0].value, 15)
        self.assertEqual(self.evaluate('16;')[0].value, 16)
        self.assertEqual(self.evaluate('17;')[0].value, 17)
        self.assertEqual(self.evaluate('18;')[0].value, 18)
        self.assertEqual(self.evaluate('19;')[0].value, 19)

    def test_decimal(self) -> None:
        self.assertEqual((1, 10), self.evaluate('0.1;')[0].as_tuple())
        self.assertEqual((1, 5),  self.evaluate('0.2;')[0].as_tuple())
        self.assertEqual((3, 10), self.evaluate('0.3;')[0].as_tuple())
        self.assertEqual((2, 5),  self.evaluate('0.4;')[0].as_tuple())
        self.assertEqual((1, 2),  self.evaluate('0.5;')[0].as_tuple())
        self.assertEqual((3, 5),  self.evaluate('0.6;')[0].as_tuple())
        self.assertEqual((7, 10), self.evaluate('0.7;')[0].as_tuple())
        self.assertEqual((4, 5),  self.evaluate('0.8;')[0].as_tuple())
        self.assertEqual((9, 10), self.evaluate('0.9;')[0].as_tuple())

        self.assertEqual((1, 100), self.evaluate('0.01;')[0].as_tuple())
        self.assertEqual((1, 50),  self.evaluate('0.02;')[0].as_tuple())
        self.assertEqual((3, 100), self.evaluate('0.03;')[0].as_tuple())
        self.assertEqual((1, 25),  self.evaluate('0.04;')[0].as_tuple())
        self.assertEqual((1, 20),  self.evaluate('0.05;')[0].as_tuple())
        self.assertEqual((3, 50),  self.evaluate('0.06;')[0].as_tuple())
        self.assertEqual((7, 100), self.evaluate('0.07;')[0].as_tuple())
        self.assertEqual((2, 25),  self.evaluate('0.08;')[0].as_tuple())
        self.assertEqual((9, 100), self.evaluate('0.09;')[0].as_tuple())

    def test_rationals(self) -> None:
        self.assertEqual((3,  2), self.evaluate('1.5;')[0].as_tuple())
        self.assertEqual((5,  2), self.evaluate('2.5;')[0].as_tuple())
        self.assertEqual((15, 4), self.evaluate('3.75;')[0].as_tuple())
        self.assertEqual((2107, 20), self.evaluate('105.35;')[0].as_tuple())


class ArithmeticTestCase(BaseTest):
    def test_addition(self) -> None:
        self.assertEqual(3, self.evaluate('1 + 2;')[0].value)
        self.assertEqual((3, 1), self.evaluate('1.0 + 2.0;')[0].as_tuple())
        self.assertEqual((3, 1), self.evaluate('1 + 2.0;')[0].as_tuple())
        self.assertEqual((3, 1), self.evaluate('1.0 + 2;')[0].as_tuple())

        self.assertEqual(1, self.evaluate('1 + 0;')[0].value)
        self.assertEqual((1, 1), self.evaluate('1.0 + 0.0;')[0].as_tuple())
        self.assertEqual((1, 1), self.evaluate('1 + 0.0;')[0].as_tuple())
        self.assertEqual((1, 1), self.evaluate('1.0 + 0;')[0].as_tuple())

        self.assertEqual((3, 10), self.evaluate('0.1 + 0.2;')[0].as_tuple())
        self.assertEqual((33, 10), self.evaluate('1.1 + 2.2;')[0].as_tuple())

    def test_subtraction(self) -> None:
        self.assertEqual(1, self.evaluate('2 - 1;')[0].value)
        self.assertEqual((1, 1), self.evaluate('2.0 - 1.0;')[0].as_tuple())
        self.assertEqual((1, 1), self.evaluate('2 - 1.0;')[0].as_tuple())
        self.assertEqual((1, 1), self.evaluate('2.0 - 1;')[0].as_tuple())

        self.assertEqual(2, self.evaluate('2 - 0;')[0].value)
        self.assertEqual((2, 1), self.evaluate('2.0 - 0.0;')[0].as_tuple())
        self.assertEqual((2, 1), self.evaluate('2 - 0.0;')[0].as_tuple())
        self.assertEqual((2, 1), self.evaluate('2.0 - 0;')[0].as_tuple())

        self.assertEqual(-2, self.evaluate('0 - 2;')[0].value)
        self.assertEqual((-2, 1), self.evaluate('0.0 - 2.0;')[0].as_tuple())
        self.assertEqual((-2, 1), self.evaluate('0 - 2.0;')[0].as_tuple())
        self.assertEqual((-2, 1), self.evaluate('0.0 - 2;')[0].as_tuple())

    def test_multiplication(self) -> None:
        self.assertEqual(6, self.evaluate('2 * 3;')[0].value)
        self.assertEqual((6, 1), self.evaluate('2.0 * 3.0;')[0].as_tuple())
        self.assertEqual((6, 1), self.evaluate('2 * 3.0;')[0].as_tuple())
        self.assertEqual((6, 1), self.evaluate('2.0 * 3;')[0].as_tuple())

        self.assertEqual(0, self.evaluate('2 * 0;')[0].value)
        self.assertEqual((0, 1), self.evaluate('2.0 * 0.0;')[0].as_tuple())
        self.assertEqual((0, 1), self.evaluate('2 * 0.0;')[0].as_tuple())
        self.assertEqual((0, 1), self.evaluate('2.0 * 0;')[0].as_tuple())

        self.assertEqual(2, self.evaluate('2 * 1;')[0].value)
        self.assertEqual((2, 1), self.evaluate('2.0 * 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), self.evaluate('2 * 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), self.evaluate('2.0 * 1;')[0].as_tuple())

    def test_division(self) -> None:
        self.assertEqual((2, 3), self.evaluate('2 / 3;')[0].as_tuple())
        self.assertEqual((2, 3), self.evaluate('2.0 / 3.0;')[0].as_tuple())
        self.assertEqual((2, 3), self.evaluate('2 / 3.0;')[0].as_tuple())
        self.assertEqual((2, 3), self.evaluate('2.0 / 3;')[0].as_tuple())

        with self.assertRaises(ZeroDivisionError):
            self.evaluate('2 / 0;')
        with self.assertRaises(ZeroDivisionError):
            self.evaluate('2.0 / 0.0;')
        with self.assertRaises(ZeroDivisionError):
            self.evaluate('2 / 0.0;')
        with self.assertRaises(ZeroDivisionError):
            self.evaluate('2.0 / 0;')

        self.assertEqual((2, 1), self.evaluate('2 / 1;')[0].as_tuple())
        self.assertEqual((2, 1), self.evaluate('2.0 / 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), self.evaluate('2 / 1.0;')[0].as_tuple())
        self.assertEqual((2, 1), self.evaluate('2.0 / 1;')[0].as_tuple())


class VariablesTestCase(BaseTest):
    def test_variable_declaration(self) -> None:
        with self.parser.context:
            self.evaluate('int x;')
            self.assertIn('x', self.parser.context)
            x = self.parser.context.get_variable('x', allow_undefined=True)
            self.assertIs(x.value, undefined)

        with self.parser.context:
            self.evaluate('int y = 5;')
            self.assertIn('y', self.parser.context)
            self.assertIsInstance(self.parser.context['y'], Integer)
            self.assertEqual(self.parser.context['y'].value, 5)

    def test_variable_definition(self) -> None:
        with self.parser.context:
            self.evaluate('int x;')
            self.evaluate('x = 5;')
            self.assertIn('x', self.parser.context)
            self.assertIsInstance(self.parser.context['x'], Integer)
            self.assertEqual(5, self.parser.context['x'].value)

    def test_variable_access(self) -> None:
        with self.parser.context:
            self.evaluate('int x = 5;')
            x = self.evaluate('x;')[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(5, x.value)

        with self.parser.context:
            with self.assertRaises(NameError):
                self.evaluate('y;')

    def test_boolean_variables(self) -> None:
        with self.parser.context:
            _true = self.evaluate('true;')[0]
            self.assertIsInstance(_true, Boolean)
            self.assertIs(_true.value, True)

        with self.parser.context:
            _false = self.evaluate('false;')[0]
            self.assertIsInstance(_false, Boolean)
            self.assertIs(_false.value, False)

    def test_nullish_variables(self) -> None:
        _undefined = self.evaluate('undefined;')[0]
        self.assertIsInstance(_undefined, Undefined)
        self.assertIs(_undefined, undefined)

        _null = self.evaluate('null;')[0]
        self.assertIsInstance(_null, Null)
        self.assertIs(_null, null)

    def test_auto_variables(self) -> None:
        with self.parser.context:
            x = self.evaluate('auto x = 5; x;')[-1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(x.value, 5)

        with self.parser.context:
            pi = self.evaluate('auto pi = 22 / 7; pi;')[-1]
            self.assertIsInstance(pi, Rational)
            self.assertEqual((22, 7), pi.as_tuple())

    def test_weird_variables(self) -> None:
        with self.parser.context:
            self.evaluate('int 0 = 1;')
            _0 = self.evaluate('0;')[0]
            self.assertIsInstance(_0, Integer)
            self.assertEqual(1, _0.value)

        with self.parser.context:
            self.evaluate('int three = 3;')
            self.evaluate('rational pi = three.14;')
            pi = self.evaluate('pi;')[0]
            self.assertIsInstance(pi, Rational)
            self.assertEqual((157, 50), pi.as_tuple())

    def test_variable_locality(self) -> None:
        with self.parser.context:
            self.evaluate('int 3 = 0; int x;')
            self.evaluate('{ nonlocal 3; x = 3; }')
            x = self.evaluate('x;')[0]
            self.assertEqual(0, x.value)

        with self.parser.context:
            self.evaluate('int 3 = 0; int x;')
            self.evaluate('{ x = 3; }')
            x = self.evaluate('x;')[0]
            self.assertEqual(3, x.value)


class OperatorTestCase(BaseTest):
    def test_increment(self) -> None:
        with self.parser.context:
            self.evaluate('auto x = 0;')
            x = self.evaluate('x++;')[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(1, x.value)
            x = self.evaluate('x++;')[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(2, x.value)

        with self.parser.context:
            self.evaluate('auto y = 0.0;')
            y = self.evaluate('y++;')[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((1, 1), y.as_tuple())
            y = self.evaluate('y++;')[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((2, 1), y.as_tuple())

    def test_decrement(self) -> None:
        with self.parser.context:
            self.evaluate('auto x = 0;')
            x = self.evaluate('x--;')[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(-1, x.value)
            x = self.evaluate('x--;')[0]
            self.assertIsInstance(x, Integer)
            self.assertEqual(-2, x.value)

        with self.parser.context:
            self.evaluate('auto y = 0.0;')
            y = self.evaluate('y--;')[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((-1, 1), y.as_tuple())
            y = self.evaluate('y--;')[0]
            self.assertIsInstance(y, Rational)
            self.assertEqual((-2, 1), y.as_tuple())

    def test_plus_equals(self) -> None:
        with self.parser.context:
            self.evaluate('auto x = 0;')
            x = self.evaluate('x += 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(2, x.value)
            x = self.evaluate('x += 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(4, x.value)

        with self.parser.context:
            self.evaluate('auto y = 0.0;')
            y = self.evaluate('y += 2; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((2, 1), y.as_tuple())
            y = self.evaluate('y += 2; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((4, 1), y.as_tuple())

    def test_minus_equals(self) -> None:
        with self.parser.context:
            self.evaluate('auto x = 0;')
            x = self.evaluate('x -= 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(-2, x.value)
            x = self.evaluate('x -= 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(-4, x.value)

        with self.parser.context:
            self.evaluate('auto y = 0.0;')
            y = self.evaluate('y -= 2; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((-2, 1), y.as_tuple())
            y = self.evaluate('y -= 2; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((-4, 1), y.as_tuple())

    def test_star_equals(self) -> None:
        with self.parser.context:
            self.evaluate('auto x = 1;')
            x = self.evaluate('x *= 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(2, x.value)
            x = self.evaluate('x *= 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(4, x.value)

        with self.parser.context:
            self.evaluate('auto y = 1.0;')
            y = self.evaluate('y *= 0.5; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((1, 2), y.as_tuple())
            y = self.evaluate('y *= 0.5; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((1, 4), y.as_tuple())

    def test_slash_equals(self) -> None:
        with self.parser.context:
            self.evaluate('auto x = 4;')
            x = self.evaluate('x /= 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(2, x.value)
            x = self.evaluate('x /= 2; x;')[1]
            self.assertIsInstance(x, Integer)
            self.assertEqual(1, x.value)

        with self.parser.context:
            self.evaluate('auto y = 1.0;')
            y = self.evaluate('y /= 2; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((1, 2), y.as_tuple())
            y = self.evaluate('y /= 2; y;')[1]
            self.assertIsInstance(y, Rational)
            self.assertEqual((1, 4), y.as_tuple())

    def test_comparison_operators(self) -> None:
        def _check(value, expect):
            self.assertIsInstance(value, Boolean)
            self.assertEqual(value, expect)

        less_1, less_2, less_3 = self.evaluate('0 < 1; 0 < 0; 1 < 0;')
        _check(less_1, true)
        _check(less_2, false)
        _check(less_3, false)

        less_equal_1, less_equal_2, less_equal_3 = self.evaluate('0 <= 1; 0 <= 0; 1 <= 0;')
        _check(less_equal_1, true)
        _check(less_equal_2, true)
        _check(less_equal_3, false)

        greater_1, greater_2, greater_3 = self.evaluate('0 > 1; 0 > 0; 1 > 0;')
        _check(greater_1, false)
        _check(greater_2, false)
        _check(greater_3, true)

        greater_equal_1, greater_equal_2, greater_equal_3 = self.evaluate('0 >= 1; 0 >= 0; 1 >= 0;')
        _check(greater_equal_1, false)
        _check(greater_equal_2, true)
        _check(greater_equal_3, true)

        equality_1, equality_2, equality_3 = self.evaluate('0 == 1; 1 == 1; 1 == 0;')
        _check(equality_1, false)
        _check(equality_2, true)
        _check(equality_3, false)

        nonequality_1, nonequality_2, nonequality_3 = self.evaluate('0 != 1; 1 != 1; 1 != 0;')
        _check(nonequality_1, true)
        _check(nonequality_2, false)
        _check(nonequality_3, true)


class ControlFlowTestCase(BaseTest):
    def test_for_loop(self) -> None:
        with self.parser.context:
            self.evaluate('int a = 1;')
            self.evaluate('for (int x = 0; x < 10; x++) { a *= 2; }')
            a = self.evaluate('a;')[0]
            self.assertEqual(1024, a.value)

    def test_while_loop(self) -> None:
        with self.parser.context:
            self.evaluate('int a = 1;')
            self.evaluate('while (a < 1000) a *= 2;')
            a = self.evaluate('a;')[0]
            self.assertEqual(1024, a.value)

    def test_if_statement(self) -> None:
        with self.parser.context:
            self.evaluate('int x = 0;')
            self.evaluate('if (true) x = 1;')
            self.assertEqual(1, self.evaluate('x;')[0].value)

        with self.parser.context:
            self.evaluate('int y = 0;')
            self.evaluate('if (false) y = 1;')
            self.assertEqual(0, self.evaluate('y;')[0].value)

    def test_if_else_statement(self) -> None:
        with self.parser.context:
            self.evaluate('int x = 0;')
            self.evaluate('if (true) x = 1; else x = 2;')
            self.assertEqual(1, self.evaluate('x;')[0].value)

        with self.parser.context:
            self.evaluate('int y = 0;')
            self.evaluate('if (false) y = 1; else y = 2;')
            self.assertEqual(2, self.evaluate('y;')[0].value)


class FunctionTestCase(BaseTest):
    def test_function_definition(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
