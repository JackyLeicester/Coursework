import io
import unittest
from typing import Any
from unittest.mock import patch

from src import Lexer, Parser, evaluate
from src.parser import IncorrectSyntax


class TestPrintFunction(unittest.TestCase):
    @staticmethod
    def _eval(src: str) -> Any:
        lexer = Lexer(src)
        parser = Parser(lexer)
        expressions = parser.run()
        return evaluate(expressions)

    def test_missing_comma(self):
        src = "print(1 'a');"
        self.assertRaises(IncorrectSyntax, self._eval, src)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_fn(self, mock_stdout):
        src = "print('a');"
        res = self._eval(src)
        self.assertEqual(res, None)
        self.assertEqual(mock_stdout.getvalue(), "a")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_println_fn(self, mock_stdout):
        src = "println(1.1);"
        res = self._eval(src)
        self.assertEqual(res, None)
        self.assertEqual(mock_stdout.getvalue(), "1.1\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_zero_argument(self, mock_stdout):
        src = "println();"
        res = self._eval(src)
        self.assertEqual(res, None)
        self.assertEqual(mock_stdout.getvalue(), "\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_single_argument(self, mock_stdout):
        src = "print(true);"
        res = self._eval(src)
        self.assertEqual(res, None)
        self.assertEqual(mock_stdout.getvalue(), "True")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_multiple_arguments(self, mock_stdout):
        src = """println(1, 1.1, 'a', "string", false);"""
        res = self._eval(src)
        self.assertEqual(res, None)
        self.assertEqual(mock_stdout.getvalue(), "1 1.1 a string False\n")


if __name__ == "__main__":
    unittest.main()
