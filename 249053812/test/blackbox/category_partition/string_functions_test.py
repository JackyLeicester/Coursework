import unittest
from typing import Any

from src import Lexer, Parser, evaluate


class TestStringFunctions(unittest.TestCase):
    @staticmethod
    def _eval(src: str) -> Any:
        lexer = Lexer(src)
        parser = Parser(lexer)
        expressions = parser.run()
        return evaluate(expressions)

    def test_trim_single_arg(self):
        result = self._eval('trim("  hello  ");')
        self.assertEqual(result, "hello")

    def test_length_single_arg(self):
        result = self._eval('length("abc");')
        self.assertEqual(result, 3)

    def test_concat_multiple_args(self):
        result = self._eval('concat("a","b");')
        self.assertEqual(result, "ab")

    def test_has_prefix_multiple_args(self):
        result = self._eval('hasPrefix("a","abc");')
        self.assertTrue(result)

    def test_has_suffix_multiple_args(self):
        result = self._eval('hasSuffix("c","abc");')
        self.assertTrue(result)

    def test_zero_arguments_error(self):
        self.assertRaises(Exception, self._eval, "concat();")


if __name__ == "__main__":
    unittest.main()
