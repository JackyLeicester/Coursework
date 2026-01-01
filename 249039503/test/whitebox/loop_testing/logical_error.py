import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestLogicalErrorLoopTesting(unittest.TestCase):
    # Case 1: Zero logical errors
    def test_zero_errors(self):
        program = """
        let x = 1;
        x = x + 1;
        x;
        """
        self.assertEqual(evaluate_expr(program), 2)

    # Case 2: One logical error
    def test_one_error_undefined_variable(self):
        program = "x;"
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("Undefined variable 'x'", str(ctx.exception))

    # Case 3: Multiple logical errors
    def test_multiple_errors_across_programs(self):
        # Error 1: undefined variable read
        with self.assertRaises(RuntimeEvaluationError):
            evaluate_expr("y;")

        # Error 2: assign to const
        with self.assertRaises(RuntimeEvaluationError):
            evaluate_expr("""
            const a = 1;
            a = 2;
            """)

        # Error 3: break outside loop
        with self.assertRaises(RuntimeEvaluationError):
            evaluate_expr("break;")


if __name__ == "__main__":
    unittest.main()
