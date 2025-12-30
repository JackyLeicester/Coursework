import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class ArithmeticOperationsBranchTest(unittest.TestCase):
    # PLUS
    def test_plus_int_int(self):
        self.assertEqual(run("1 + 2;"), 3)

    def test_plus_float_float(self):
        self.assertAlmostEqual(run("1.5 + 2.25;"), 3.75)

    def test_plus_int_float(self):
        self.assertAlmostEqual(run("1 + 2.5;"), 3.5)

    def test_plus_float_int(self):
        self.assertAlmostEqual(run("2.5 + 1;"), 3.5)

    # MINUS
    def test_minus_int_int(self):
        self.assertEqual(run("5 - 2;"), 3)

    def test_minus_unary(self):
        self.assertEqual(run("-5;"), -5)

    # MULTIPLY
    def test_multiply_int_int(self):
        self.assertEqual(run("3 * 4;"), 12)

    def test_multiply_float_int(self):
        self.assertAlmostEqual(run("2.5 * 4;"), 10.0)

    # DIVIDE
    def test_divide_int_int_exact(self):
        self.assertEqual(run("10 / 2;"), 5)

    def test_divide_float(self):
        self.assertAlmostEqual(run("7.5 / 2.5;"), 3.0)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(Exception):
            run("10 / 0;")

    def test_divide_by_zero_float_raises(self):
        with self.assertRaises(Exception):
            run("10.0 / 0.0;")

    # PARSER BRANCHES
    def test_precedence_mul_before_add(self):
        self.assertEqual(run("1 + 2 * 3;"), 7)

    def test_parentheses_override_precedence(self):
        self.assertEqual(run("(1 + 2) * 3;"), 9)

    def test_left_associative_subtraction(self):
        self.assertEqual(run("10 - 3 - 2;"), 5)

    def test_left_associative_division(self):
        self.assertEqual(run("20 / 2 / 2;"), 5)
