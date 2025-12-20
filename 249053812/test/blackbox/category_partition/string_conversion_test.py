import unittest
from typing import Any

from src import Lexer, Parser, evaluate


class TestConversionFunctions(unittest.TestCase):
    @staticmethod
    def _eval(src: str) -> Any:
        lexer = Lexer(src)
        parser = Parser(lexer)
        expressions = parser.run()
        return evaluate(expressions)

    def test_is_int_function(self):
        result = self._eval('isInt("123");')
        self.assertIsInstance(result, bool)

    def test_to_int_function(self):
        result = self._eval('toInt("42");')
        self.assertIsInstance(result, int)
        self.assertEqual(result, 42)

    def test_is_float_function(self):
        result = self._eval('isFloat("3.14");')
        self.assertIsInstance(result, bool)

    def test_to_float_function(self):
        result = self._eval('toFloat("2.5");')
        self.assertIsInstance(result, float)
        self.assertEqual(result, 2.5)

    def test_to_str_function(self):
        result = self._eval("toStr(100);")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "100")

    def test_return_type_str(self):
        result = self._eval("toStr(3.14);")
        self.assertIsInstance(result, str)

    def test_return_type_float(self):
        result = self._eval('toFloat("1.1");')
        self.assertIsInstance(result, float)

    def test_return_type_int(self):
        result = self._eval('toInt("7");')
        self.assertIsInstance(result, int)

    def test_zero_arguments(self):
        self.assertRaises(Exception, self._eval, "isInt();")

    def test_single_argument(self):
        result = self._eval('isFloat("0.5");')
        self.assertIsInstance(result, bool)

    def test_multiple_arguments(self):
        self.assertRaises(Exception, self._eval, 'isFloat("1.1", "2.2");')


if __name__ == "__main__":
    unittest.main()
