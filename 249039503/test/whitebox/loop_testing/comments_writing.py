import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestExitStatementLoopTesting(unittest.TestCase):
    def test_exit_zero_statements_before(self):
        self.assertEqual(evaluate_expr("exit(1);"), 1)

    def test_exit_one_statement_before(self):
        program = """
        let x = 10;
        exit(2);
        """
        self.assertEqual(evaluate_expr(program), 2)

    def test_exit_multiple_statements_before(self):
        program = """
        let x = 1;
        x = x + 1;
        x = x + 1;
        exit(3);
        """
        self.assertEqual(evaluate_expr(program), 3)


if __name__ == "__main__":
    unittest.main()
