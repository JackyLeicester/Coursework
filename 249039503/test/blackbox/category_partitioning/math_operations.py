import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import _eval


class MathOperationsTest(unittest.TestCase):
    def _eval(self, expr: str):
        lexer = Lexer(expr)
        parser = Parser(lexer)
        expressions = parser.run()
        env = {}
        result = None
        for e in expressions:
            if e is None:
                continue
            result = _eval(e, env)
        return result

    def test_simple_expression_with_plus_1(self):
        self.assertEqual(self._eval("100 + 2 + 3"), 105)

    def test_simple_expression_combined_2(self):
        self.assertEqual(self._eval("1 * 25 + 3"), 28)

    def test_simple_expression_combined_3(self):
        self.assertEqual(self._eval("10 * 12 * 3 + 4"), 364)

    def test_combined_alt_digit_4(self):
        self.assertEqual(self._eval("-10 + 2 + 3 - 4 - 5"), -14)

    def test_combined_minus_plus_5(self):
        self.assertEqual(self._eval("12 + 23 - 43 + 44"), 36)

    def test_combined_division_multiplication_plus6(self):
        self.assertEqual(self._eval("88 / 2 * 4 + 212"), 388)

    def test_combined_7(self):
        self.assertEqual(self._eval("1 + 2 * 3 - 2 + 4 / 2"), 7)

    def test_simple_plus_8(self):
        self.assertEqual(self._eval("111 + 222 * 223"), 49617)

    def test_multiplication_by_zero_9(self):
        self.assertEqual(self._eval("0 * 1 + 2 * 0"), 0)

    def test_minus_signed_digit_10(self):
        self.assertEqual(self._eval("-11 + 20 * 3"), 49)

    def test_several_minus_digits_11(self):
        self.assertEqual(self._eval("(-1) + 2 * (-3)"), -7)

    def test_nested_operation_12(self):
        self.assertEqual(self._eval("(10 + 2) * 30 + 4"), 364)

    def test_sqrt(self):
        self.assertEqual(self._eval("sqrt(900);"), 30.0)

    def test_pow(self):
        self.assertEqual(self._eval("pow(20,3);"), 800.0)

    def test_ceil(self):
        self.assertEqual(self._eval("ceil(2.3);"), 3)

    def test_floor(self):
        self.assertEqual(self._eval("floor(2.9);"), 2)

    def test_abs_positive(self):
        self.assertEqual(self._eval("abs(5);"), 5)

    def test_abs_negative(self):
        self.assertEqual(self._eval("abs(-5);"), 5)


if __name__ == "__main__":
    unittest.main()
