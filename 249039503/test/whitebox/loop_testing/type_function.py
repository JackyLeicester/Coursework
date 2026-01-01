import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestTypeFunctionLoopTesting(unittest.TestCase):
    # Case 1: Zero type() calls
    def test_zero_type_calls(self):
        program = """
        let x = 5;
        x;
        """
        self.assertEqual(evaluate_expr(program), 5)

    # Case 2: One type() call
    def test_one_type_call(self):
        program = "type(10);"
        self.assertEqual(evaluate_expr(program), "integer")

    # Case 3: Multiple type() calls
    def test_multiple_type_calls(self):
        program = """
        let a = type(1);
        let b = type(1.5);
        let c = type("x");
        a + b + c;
        """
        self.assertEqual(evaluate_expr(program), "integerfloatstring")


if __name__ == "__main__":
    unittest.main()
