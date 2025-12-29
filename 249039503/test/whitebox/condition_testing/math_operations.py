import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestMathOperationsCondition(unittest.TestCase):
    def test_sqrt_valid_int(self):
        self.assertAlmostEqual(evaluate_expr("sqrt(9);"), 3.0, places=6)

    def test_sqrt_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("sqrt(1, 2);")
        self.assertIn("sqrt expects 1 arguments", str(ctx.exception))

    def test_sqrt_negative_raises(self):
        with self.assertRaises(Exception):
            evaluate_expr("sqrt(-1);")

    def test_pow_valid(self):
        self.assertAlmostEqual(evaluate_expr("pow(2, 3);"), 8.0, places=6)

    def test_pow_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("pow(2);")
        self.assertIn("pow expects 2 arguments", str(ctx.exception))

    def test_ceil_valid(self):
        self.assertEqual(evaluate_expr("ceil(2.1);"), 3)

    def test_ceil_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("ceil();")
        self.assertIn("ceil expects 1 arguments", str(ctx.exception))

    def test_floor_valid(self):
        self.assertEqual(evaluate_expr("floor(2.9);"), 2)

    def test_floor_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("floor(1, 2);")
        self.assertIn("floor expects 1 arguments", str(ctx.exception))

    def test_abs_valid_int(self):
        self.assertEqual(evaluate_expr("abs(-5);"), 5)

    def test_abs_valid_float(self):
        self.assertAlmostEqual(evaluate_expr("abs(-2.5);"), 2.5, places=6)

    def test_abs_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("abs(1, 2);")
        self.assertIn("abs expects 1 arguments", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
