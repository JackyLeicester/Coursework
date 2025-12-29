import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestArithmeticOperationsStatement(unittest.TestCase):
    def test_int_literal(self):
        self.assertEqual(evaluate_expr("5;"), 5)

    def test_float_literal(self):
        self.assertEqual(evaluate_expr("1.5;"), 1.5)

    def test_prefix_minus(self):
        self.assertEqual(evaluate_expr("-5;"), -5)

    def test_prefix_plus(self):
        self.assertEqual(evaluate_expr("+5;"), 5)

    def test_prefix_not(self):
        self.assertEqual(evaluate_expr("!null;"), True)

    def test_infix_plus(self):
        self.assertEqual(evaluate_expr("1 + 2;"), 3)

    def test_infix_minus(self):
        self.assertEqual(evaluate_expr("5 - 8;"), -3)

    def test_infix_multiply(self):
        self.assertEqual(evaluate_expr("3 * 4;"), 12)

    def test_infix_divide_nonzero(self):
        self.assertEqual(evaluate_expr("10 / 2;"), 5)

    def test_division_by_zero_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("10 / 0;")
        self.assertIn("Division by zero", str(ctx.exception))

    def test_bitwise_and_ints(self):
        self.assertEqual(evaluate_expr("5 & 3;"), 1)

    def test_bitwise_requires_integers_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("1.5 & 1;")
        self.assertIn("Bitwise operations require integers", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
