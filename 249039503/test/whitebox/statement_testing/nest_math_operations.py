import unittest

from src.lexer import Lexer
from src.parser import Parser, IncorrectSyntax
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestNestMathOperationsStatement(unittest.TestCase):
    def test_nested_parentheses(self):
        self.assertEqual(evaluate_expr("1 + (2 * (3 + 4));"), 15)

    def test_operator_precedence(self):
        self.assertEqual(evaluate_expr("1 + 2 * 3;"), 7)

    def test_deep_nesting(self):
        self.assertEqual(evaluate_expr("((1 + 2) + (3 + 4)) * (2 + 3);"), 50)

    def test_mixed_ops_nested(self):
        self.assertEqual(evaluate_expr("(20 / (2 * 2)) - (3 + 1);"), 1)

    def test_missing_closing_paren_raises(self):
        with self.assertRaises(IncorrectSyntax):
            Parser(Lexer("1 + (2 * (3 + 4);")).run()


if __name__ == "__main__":
    unittest.main()
