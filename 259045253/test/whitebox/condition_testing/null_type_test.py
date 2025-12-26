import io
import unittest
from typing import Any
from unittest.mock import patch

from src import Parser, Lexer, evaluate
from src.parser import NullLiteral
from src.tokens import Token


class TestNullLiteral(unittest.TestCase):
    """
    This class performs condition testing on the following:
    - `null` branch in `_read_identifier` of the `Lexer`.
    - `parse_null` method of `Parser`.
    - Evaluating of "null" statements in `evaluator`

    This corresponds to user story number: #109
    <https://github.com/JackyLeicester/Coursework/issues/109>

    There is only one input that we can control i.e. the input string while
    instantiating the `Lexer` class.
    """

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

    # Test 1: branch `case "null"` in `_read_identifier` of `Lexer`
    def test_lexer1(self):
        lexer = Lexer("null")
        (token, _str_repr) = lexer.next_token()
        self.assertEqual(token, Token.NULL)

    # Test 1: `parse_null` method
    def test_parser1(self):
        parser = self.setup_parser("null;")
        null = parser.parse_null()
        self.assertIsInstance(null, NullLiteral)
        self.assertEqual(null.literal, "null")

    # Test 1: `NullLiteral` handling branch in `evaluate` function
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_evaluator1(self, mock_stdout):
        result = self.eval("print(null);")
        self.assertEqual(result, None)
        self.assertEqual(mock_stdout.getvalue(), "None")


if __name__ == "__main__":
    unittest.main()
