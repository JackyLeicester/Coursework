import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestLogicalErrorStatement(unittest.TestCase):
    def test_undefined_variable_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("x;")
        self.assertIn("Undefined variable", str(ctx.exception))

    def test_assignment_lhs_not_identifier_raises(self):
        program = "(1 + 2) = 3;"
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn(
            "Left-hand side of assignment must be a variable",
            str(ctx.exception),
        )

    def test_division_by_zero_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("10 / 0;")
        self.assertIn("Division by zero", str(ctx.exception))

    def test_break_outside_loop_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("break;")
        self.assertIn("break used outside loop", str(ctx.exception))

    def test_continue_outside_loop_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("continue;")
        self.assertIn("continue used outside loop", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
