import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestExitStatementStatement(unittest.TestCase):
    def test_exit_returns_code(self):
        self.assertEqual(evaluate_expr("exit(7);"), 7)

    def test_exit_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("exit(1, 2);")
        self.assertIn("exit expects 1 argument", str(ctx.exception))

    def test_exit_bool_argument_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("exit(true);")
        self.assertIn("argument must be int", str(ctx.exception))

    def test_exit_float_argument_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("exit(1.5);")
        self.assertIn("argument must be int", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
