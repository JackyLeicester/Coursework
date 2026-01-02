import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestForLoopTesting(unittest.TestCase):
    # Case 1: Zero iterations
    def test_for_zero_iterations(self):
        program = """
        let sum = 0;
        for(let i = 0; i < 0; i = i + 1) {
            sum = sum + i;
        }
        sum;
        """
        self.assertEqual(evaluate_expr(program), 0)

    # Case 2: One iteration
    def test_for_one_iteration(self):
        program = """
        let sum = 0;
        for(let i = 0; i < 1; i = i + 1) {
            sum = sum + i;
        }
        sum;
        """
        self.assertEqual(evaluate_expr(program), 0)

    # Case 3: Multiple iterations
    def test_for_multiple_iterations(self):
        program = """
        let sum = 0;
        for(let i = 0; i < 5; i = i + 1) {
            sum = sum + i;
        }
        sum;
        """
        self.assertEqual(evaluate_expr(program), 10)  # 0+1+2+3+4=10


if __name__ == "__main__":
    unittest.main()
