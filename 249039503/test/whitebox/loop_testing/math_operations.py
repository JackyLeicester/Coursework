import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestMathOperationsLoopTesting(unittest.TestCase):
    # Case 1: Zero math operations
    def test_zero_math_operations(self):
        program = "1 + 2;"
        self.assertEqual(evaluate_expr(program), 3)

    # Case 2: One math operation
    def test_one_math_operation(self):
        program = "sqrt(9);"
        self.assertEqual(evaluate_expr(program), 3.0)

    # Case 3: Multiple math operations
    def test_multiple_math_operations(self):
        program = """
        let a = sqrt(9);
        let b = pow(2, 3);
        let c = abs(-5);
        a + b + c;
        """
        self.assertEqual(evaluate_expr(program), 16.0)


if __name__ == "__main__":
    unittest.main()
