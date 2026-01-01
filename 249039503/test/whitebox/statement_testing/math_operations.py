import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestMathOperationsStatement(unittest.TestCase):
    def test_sqrt_success(self):
        self.assertEqual(evaluate_expr("sqrt(9);"), 3.0)

    def test_sqrt_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("sqrt(9, 1);")
        self.assertIn("sqrt expects 1 arguments", str(ctx.exception))

    def test_pow_success(self):
        self.assertEqual(evaluate_expr("pow(2, 3);"), 8.0)

    def test_pow_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("pow(2);")
        self.assertIn("pow expects 2 arguments", str(ctx.exception))

    def test_ceil_success(self):
        self.assertEqual(evaluate_expr("ceil(1.2);"), 2)

    def test_ceil_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("ceil(1.2, 2.3);")
        self.assertIn("ceil expects 1 arguments", str(ctx.exception))

    def test_floor_success(self):
        self.assertEqual(evaluate_expr("floor(1.8);"), 1)

    def test_floor_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("floor();")
        self.assertIn("floor expects 1 arguments", str(ctx.exception))

    def test_abs_int_success(self):
        self.assertEqual(evaluate_expr("abs(-5);"), 5)

    def test_abs_float_success(self):
        self.assertEqual(evaluate_expr("abs(-2.5);"), 2.5)

    def test_abs_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("abs(1, 2);")
        self.assertIn("abs expects 1 arguments", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
