import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestArithmeticOperationsLoopTesting(unittest.TestCase):
    # Zero arithmetic operations
    def test_zero_operations_single_literal(self):
        self.assertEqual(evaluate_expr("5;"), 5)

    #  One arithmetic operation
    def test_one_operation(self):
        self.assertEqual(evaluate_expr("5 + 2;"), 7)

    # Multiple arithmetic operations
    def test_multiple_operations_chain(self):
        self.assertEqual(evaluate_expr("1 + 2 * 3 - 4;"), 3)

    #  many case
    def test_multiple_operations_nested(self):
        self.assertEqual(evaluate_expr("(1 + 2) * (3 + 4);"), 21)


if __name__ == "__main__":
    unittest.main()
