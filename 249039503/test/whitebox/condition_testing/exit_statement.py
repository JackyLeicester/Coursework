import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestExitStatementCondition(unittest.TestCase):
    def test_exit_with_int_returns_code(self):
        program = "exit(7);"
        self.assertEqual(evaluate_expr(program), 7)

    def test_exit_with_zero_args_raises(self):
        program = "exit();"
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("exit expects 1 argument", str(ctx.exception))

    def test_exit_with_two_args_raises(self):
        program = "exit(1, 2);"
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("exit expects 1 argument", str(ctx.exception))

    def test_exit_with_bool_raises(self):
        program = "exit(true);"
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("eixt argument must be int", str(ctx.exception))

    def test_exit_with_float_raises(self):
        program = "exit(1.5);"
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("eixt argument must be int", str(ctx.exception))

    def test_exit_with_string_raises(self):
        program = 'exit("1");'
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("eixt argument must be int", str(ctx.exception))

    def test_exit_short_circuits_program(self):
        program = """
        exit(3);
        1 / 0;
        """
        self.assertEqual(evaluate_expr(program), 3)


if __name__ == "__main__":
    unittest.main()
