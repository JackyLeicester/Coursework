import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError

"""
Tests focus on condition testing which cover all feasible outcomes
of conditions in evaluator decision points in arithmetic operations
"""

def run(code: str):
    expressions = Parser(Lexer(code)).run()
    return evaluate(expressions)


class TestArithmeticOperationsCondition(unittest.TestCase):

    def test_division_right_nonzero_int(self):
        self.assertEqual(run("10/2;"), 5)

    def test_division_right_zero_int_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            run("10/0;")
        self.assertIn("Division by zero", str(ctx.exception))

    def test_division_right_zero_float_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            run("10.0/0.0;")
        self.assertIn("Division by zero", str(ctx.exception))

    def test_division_right_nonzero_float(self):
        self.assertEqual(run("7.5/2.5;"), 3.0)

    def test_plus_int_int(self):
        self.assertEqual(run("1+2;"), 3)

    def test_minus_int_int(self):
        self.assertEqual(run("5-8;"), -3)

    def test_multiply_int_int(self):
        self.assertEqual(run("3*4;"), 12)

    def test_plus_int_float(self):
        # Python semantics: int + float -> float
        self.assertEqual(run("1+2.5;"), 3.5)

    def test_multiply_float_int(self):
        self.assertEqual(run("2.5*2;"), 5.0)

    def test_prefix_minus_number(self):
        self.assertEqual(run("-5;"), -5)

    def test_prefix_plus_number(self):
        self.assertEqual(run("+5;"), 5)

    def test_prefix_not_truthy(self):
        self.assertEqual(run("!1;"), False)

    def test_prefix_not_falsy(self):
        self.assertEqual(run("!null;"), True)

    def test_plus_string_and_int_raises(self):
        with self.assertRaises(Exception):
            run('"a"+1;')

    def test_bitwise_and_requires_integers_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            run("1.5 & 1;")
        self.assertIn("Bitwise operations require integers",
                      str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
