import io
import unittest
from typing import Any
from unittest.mock import patch

from src.parser import CallExpression, IntegerLiteral, Identifier
from src import Lexer, Parser, evaluate
from src.tokens import Token


class TestPrintFunction(unittest.TestCase):
    @staticmethod
    def eval(src: str) -> Any:
        lexer = Lexer(src)
        parser = Parser(lexer)
        expressions = parser.run()
        return evaluate(expressions)

    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    # Test 1: case _ in `_read_identifier`
    def test_lexer1(self):
        lexer = Lexer("print(1)")
        (token, str_repr) = lexer.next_token()
        self.assertEqual(token, Token.IDENTIFIER)
        self.assertEqual(str_repr, "print")

    # Test 2: case _ in `_read_identifier`
    def test_lexer2(self):
        lexer = Lexer("println(1)")
        (token, str_repr) = lexer.next_token()
        self.assertEqual(token, Token.IDENTIFIER)
        self.assertEqual(str_repr, "println")

    # Test 1: `parse_identifier_or_callexpression` and `parse_callexpression`
    # methods
    def test_parser1(self):
        parser = self.setup_parser("print(1);")
        print_expr = parser.parse_identifier_or_callexpression()
        self.assertIsInstance(print_expr, CallExpression)
        self.assertEqual(print_expr.identifier_name, "print")
        self.assertEqual(print_expr.parameters, [IntegerLiteral(value=1)])

    # Test 2: `parse_identifier_or_callexpression` and `parse_callexpression`
    # methods
    def test_parser2(self):
        parser = self.setup_parser("println(1, x);")
        print_expr = parser.parse_identifier_or_callexpression()
        self.assertIsInstance(print_expr, CallExpression)
        self.assertEqual(print_expr.identifier_name, "println")
        self.assertEqual(
            print_expr.parameters, [IntegerLiteral(value=1), Identifier(name="x")]
        )

    # Test 1: `CallExpression` handling for `elif name == "print"` branch in
    # `evaluate` function
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_evaluator1(self, mock_stdout):
        result = self.eval("print(1);")
        self.assertEqual(result, None)
        self.assertEqual(mock_stdout.getvalue(), "1")

    # Test 2: `CallExpression` handling for `elif name == "println"` branch in
    # `evaluate` function
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_evaluator2(self, mock_stdout):
        result = self.eval('println("foo");')
        self.assertEqual(result, None)
        self.assertEqual(mock_stdout.getvalue(), "foo\n")


if __name__ == "__main__":
    unittest.main()
