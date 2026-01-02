import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestIfConditionTesting(unittest.TestCase):
    # Test 1: Condition evaluates to true, execute consequence
    def test_if_true(self):
        program = """
        if (true) {
            42;
        } else {
            0;
        }
        """
        self.assertEqual(evaluate_expr(program), 42)

    # Test 2: Condition evaluates to false, execute alternative
    def test_if_false(self):
        program = """
        if (false) {
            42;
        } else {
            0;
        }
        """
        self.assertEqual(evaluate_expr(program), 0)

    # Test 3: Condition with expression, true
    def test_if_expression_true(self):
        program = """
        if (1 < 2) {
            "yes";
        } else {
            "no";
        }
        """
        self.assertEqual(evaluate_expr(program), "yes")

    # Test 4: Condition with expression, false
    def test_if_expression_false(self):
        program = """
        if (1 > 2) {
            "yes";
        } else {
            "no";
        }
        """
        self.assertEqual(evaluate_expr(program), "no")

    # Test 5: Nested if conditions
    def test_nested_if(self):
        program = """
        if (true) {
            if (false) {
                1;
            } else {
                2;
            }
        } else {
            3;
        }
        """
        self.assertEqual(evaluate_expr(program), 2)


if __name__ == "__main__":
    unittest.main()