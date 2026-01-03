import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class ArithmeticOperationsBranchTest(unittest.TestCase):
    # PLUS
    def test_plus_int_int_1(self):
        self.assertEqual(run("1 + 2;"), 3)

    def test_plus_float_float_2(self):
        self.assertAlmostEqual(run("1.5 + 2.25;"), 3.75)

    def test_plus_int_float_3(self):
        self.assertAlmostEqual(run("1 + 2.5;"), 3.5)

    def test_plus_float_int_4(self):
        self.assertAlmostEqual(run("2.5 + 1;"), 3.5)

    # MINUS
    def test_minus_int_int_5(self):
        self.assertEqual(run("5 - 2;"), 3)

    def test_minus_unary_6(self):
        self.assertEqual(run("-5;"), -5)

    # MULTIPLY
    def test_multiply_int_int_7(self):
        self.assertEqual(run("3 * 4;"), 12)

    def test_multiply_float_int_8(self):
        self.assertAlmostEqual(run("2.5 * 4;"), 10.0)

    # DIVIDE
    def test_divide_int_int_exact_9(self):
        self.assertEqual(run("10 / 2;"), 5)

    def test_divide_float_10(self):
        self.assertAlmostEqual(run("7.5 / 2.5;"), 3.0)

    def test_divide_by_zero_raises_11(self):
        with self.assertRaises(Exception):
            run("10 / 0;")

    def test_divide_by_zero_float_raises_12(self):
        with self.assertRaises(Exception):
            run("10.0 / 0.0;")
