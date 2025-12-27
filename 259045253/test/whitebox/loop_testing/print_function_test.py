import io
import unittest
from typing import Any
from unittest.mock import patch

from src import Lexer, Parser, evaluate


class TestPrintFunction(unittest.TestCase):
    """
    This class performs condition testing on the following:
    - default branch in `_read_identifier` of the `Lexer`.
    - `parse_identifier_or_callexpression` method of `Parser`.
    - `parse_callexpression` method of `Parser`.
    - Evaluating of functions (specifically `print` and `println`) in `evaluator`

    This corresponds to user story number: #10
    <https://github.com/JackyLeicester/Coursework/issues/10>

    There is only one input that we can control i.e. the input string while
    instantiating the `Lexer` class.
    """

    @staticmethod
    def eval(src: str) -> Any:
        lexer = Lexer(src)
        parser = Parser(lexer)
        expressions = parser.run()
        return evaluate(expressions)

    # Test 1: Test `while` loop in `parse_callexpression`, true branch
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_evaluator1(self, mock_stdout):
        result = self.eval("println('a', 'b', 1, 1.1);")
        self.assertEqual(result, None)
        self.assertEqual(mock_stdout.getvalue(), "a b 1 1.1\n")

    # Test 2: Test `while` loop in `parse_callexpression`, false branch
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_evaluator2(self, mock_stdout):
        result = self.eval("println('a');")
        self.assertEqual(result, None)
        self.assertEqual(mock_stdout.getvalue(), "a\n")


if __name__ == "__main__":
    unittest.main()
