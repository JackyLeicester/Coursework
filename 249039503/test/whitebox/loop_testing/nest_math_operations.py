import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestNestMathOperationsLoopTesting(unittest.TestCase):
    # Case 1: Zero nesting
    def test_zero_nesting(self):
        program = "1 + 2 * 3;"
        # precedence: 1 + (2*3) = 7
        self.assertEqual(evaluate_expr(program), 7)

    # Case 2: One level of nesting
    def test_one_level_nesting(self):
        program = "(1 + 2) * 3;"
        self.assertEqual(evaluate_expr(program), 9)

    # Case 3: Multiple levels of nesting
    def test_multiple_levels_nesting(self):
        program = "((1 + 2) * (3 + 4)) - (5 - (1 + 1));"
        # ((3) * (7)) - (5 - 2) = 21 - 3 = 18
        self.assertEqual(evaluate_expr(program), 18)


if __name__ == "__main__":
    unittest.main()
