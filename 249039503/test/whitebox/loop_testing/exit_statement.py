import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestExitStatementLoopTesting(unittest.TestCase):
    # Zero statements before exit
    def test_exit_zero_statements(self):
        self.assertEqual(evaluate_expr("exit(1);"), 1)

    # 1 statement before exit
    def test_exit_one_statement(self):
        program = """
        let x = 10;
        exit(2);
        """
        self.assertEqual(evaluate_expr(program), 2)

    # Multiple statements before exit
    def test_exit_multiple_statements(self):
        program = """
        let x = 1;
        x = x + 1;
        x = x + 1;
        exit(3);
        """
        self.assertEqual(evaluate_expr(program), 3)


if __name__ == "__main__":
    unittest.main()
