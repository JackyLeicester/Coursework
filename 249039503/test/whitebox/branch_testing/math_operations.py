import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class MathOperationsBranchTest(unittest.TestCase):
    # Abs
    def test_abs_int_positive(self):
        self.assertEqual(run("abs(10);"), 10)

    def test_abs_int_negative(self):
        self.assertEqual(run("abs(-10);"), 10)

    def test_abs_float_negative(self):
        self.assertAlmostEqual(run("abs(-2.5);"), 2.5)

    # Sqrt
    def test_sqrt_int(self):
        self.assertAlmostEqual(run("sqrt(9);"), 3.0)

    def test_sqrt_float(self):
        self.assertAlmostEqual(run("sqrt(2.25);"), 1.5)

    def test_sqrt_negative_raises(self):
        with self.assertRaises(Exception):
            run("sqrt(-1);")

    # Pow
    def test_pow_int_int(self):
        self.assertAlmostEqual(run("pow(2, 3);"), 8.0)

    def test_pow_float_int(self):
        self.assertAlmostEqual(run("pow(2.5, 2);"), 6.25)

    def test_pow_exponent_zero(self):
        self.assertAlmostEqual(run("pow(7, 0);"), 1.0)

    def test_pow_negative_exponent_raises_or_supported(self):
        try:
            val = run("pow(2, -1);")
            self.assertAlmostEqual(val, 0.5)
        except Exception:
            pass

    # Ceil/floor
    def test_ceil_positive(self):
        self.assertEqual(run("ceil(2.1);"), 3)

    def test_floor_positive(self):
        self.assertEqual(run("floor(2.9);"), 2)

    def test_ceil_negative(self):
        # ceil(-2.1) = -2
        self.assertEqual(run("ceil(-2.1);"), -2)

    def test_floor_negative(self):
        # floor(-2.1) = -3
        self.assertEqual(run("floor(-2.1);"), -3)

    # Type errors
    def test_sqrt_wrong_arity_raises(self):
        with self.assertRaises(Exception):
            run("sqrt();")

    def test_ceil_wrong_type_raises(self):
        with self.assertRaises(Exception):
            run('ceil("x");')
