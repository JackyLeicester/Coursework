import unittest
from unittest.mock import patch
import io

from src import Lexer, Parser, evaluate
from src.parser import IfExpression, BooleanLiteral, BlockStatement
from src.tokens import Token


class TestIfStatement(unittest.TestCase):
    """
    This class performs condition testing on the following:
    - `if` and `else` branch in `_read_identifier` of the `Lexer`.
    - `parse_if_expression` method of `Parser`.
    - Evaluating of "if" statements in `evaluator`

    This corresponds to user story number: #26
    <https://github.com/JackyLeicester/Coursework/issues/26>

    There is only one input that we can control i.e. the input string while
    instantiating the `Lexer` class.
    """

    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    # Test 1: case "if"
    def test_lexer1(self):
        lexer = Lexer("if")
        (token, _str_repr) = lexer.next_token()
        self.assertEqual(token, Token.IF)

    # Test 2: case "else"
    def test_lexer2(self):
        lexer = Lexer("else")
        (token, _str_repr) = lexer.next_token()
        self.assertEqual(token, Token.ELSE)

    # Test 1: `parse_if_expression` method
    def test_parser1(self):
        parser = self.setup_parser("""
        if true {}
        """)
        if_expr = parser.parse_if_expression()
        self.assertIsInstance(if_expr, IfExpression)
        self.assertIsInstance(if_expr.condition, BooleanLiteral)
        self.assertEqual(if_expr.condition.literal, True)
        self.assertIsInstance(if_expr.consequence, BlockStatement)
        self.assertEqual(if_expr.alternative, None)

    # Test 2: `parse_if_expression` method with `else` block
    def test_parser2(self):
        parser = self.setup_parser("""
        if true {} else {}
        """)
        if_expr = parser.parse_if_expression()
        self.assertIsInstance(if_expr, IfExpression)
        self.assertIsInstance(if_expr.condition, BooleanLiteral)
        self.assertEqual(if_expr.condition.literal, True)
        self.assertIsInstance(if_expr.consequence, BlockStatement)
        self.assertIsInstance(if_expr.alternative, BlockStatement)

    # Test 1: `IfExpression` handling in `evaluate` function
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_evaluator1(self, mock_stdout):
        parser = self.setup_parser("""
        if true { print(1) }
        """)
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(result, None)
        self.assertEqual(mock_stdout.getvalue(), "1")

    # Test 2: `IfExpression` handling in `evaluate` function with `else` block
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_evaluator2(self, mock_stdout):
        parser = self.setup_parser("""
        if false { print(1) } else { print(2) }
        """)
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(result, None)
        self.assertEqual(mock_stdout.getvalue(), "2")


if __name__ == "__main__":
    unittest.main()
