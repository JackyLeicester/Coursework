import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestBreakLoopTesting(unittest.TestCase):
    # Case 1: Zero iterations
    def test_break_zero_iterations(self):
        program = """
        for(let i = 0; i < 0; i = i + 1) {
            break;
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 0)

    # Case 2: One iteration
    def test_break_one_iteration(self):
        program = """
        for(let i = 0; i < 5; i = i + 1) {
            break;
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 0)

    # Case 3: Multiple iterations
    def test_break_multiple_iterations(self):
        program = """
        for(let i = 0; i < 10; i = i + 1) {
            if (i == 3) {
                break;
            }
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 3)


if __name__ == "__main__":
    unittest.main()