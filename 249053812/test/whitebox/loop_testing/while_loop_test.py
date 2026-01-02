import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestWhileLoopTesting(unittest.TestCase):
    # Case 1: Zero iterations
    def test_while_zero_iterations(self):
        program = """
        let sum = 0;
        let i = 0;
        while(i < 0) {
            sum = sum + i;
            i = i + 1;
        }
        sum;
        """
        self.assertEqual(evaluate_expr(program), 0)

    # Case 2: One iteration
    def test_while_one_iteration(self):
        program = """
        let sum = 0;
        let i = 0;
        while(i < 1) {
            sum = sum + i;
            i = i + 1;
        }
        sum;
        """
        self.assertEqual(evaluate_expr(program), 0)

    # Case 3: Multiple iterations
    def test_while_multiple_iterations(self):
        program = """
        let sum = 0;
        let i = 0;
        while(i < 5) {
            sum = sum + i;
            i = i + 1;
        }
        sum;
        """
        self.assertEqual(evaluate_expr(program), 10)  # 0+1+2+3+4=10


if __name__ == "__main__":
    unittest.main()
