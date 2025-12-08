import unittest

from src.lexer import Lexer
from src.tokens import Token


class TestArithmeticOperations(unittest.TestCase):
    """
    Category-partition tests for basic arithmetic operators
    (+, -, *, /) on integer and float literals.

    We test that the LEXER correctly produces the expected
    sequence of tokens; we do not evaluate expressions here.
    """

    def _tokens(self, text: str):
        """Return list of (Token, value) pairs for the given source."""
        lexer = Lexer(text)
        result = []
        tok, val = lexer.next_token()
        while tok is not Token.EOF:
            result.append((tok, val))
            tok, val = lexer.next_token()
        return result

    # ---------- INT op INT ----------

    def test_int_addition(self):
        tokens = self._tokens("1+2")
        expected = [
            (Token.INT, "1"),
            (Token.PLUS, "+"),
            (Token.INT, "2"),
        ]
        self.assertEqual(tokens, expected)

    def test_int_subtraction(self):
        tokens = self._tokens("2-1")
        expected = [
            (Token.INT, "2"),
            (Token.MINUS, "-"),
            (Token.INT, "1"),
        ]
        self.assertEqual(tokens, expected)

    def test_int_multiplication(self):
        tokens = self._tokens("3*4")
        expected = [
            (Token.INT, "3"),
            (Token.ASTERISK, "*"),
            (Token.INT, "4"),
        ]
        self.assertEqual(tokens, expected)

    def test_int_division(self):
        tokens = self._tokens("8/2")
        expected = [
            (Token.INT, "8"),
            (Token.SLASH, "/"),
            (Token.INT, "2"),
        ]
        self.assertEqual(tokens, expected)

    # ---------- FLOAT op FLOAT ----------

    def test_float_addition(self):
        tokens = self._tokens("1.5+2.5")
        expected = [
            (Token.FLOAT, "1.5"),
            (Token.PLUS, "+"),
            (Token.FLOAT, "2.5"),
        ]
        self.assertEqual(tokens, expected)

    def test_float_subtraction(self):
        tokens = self._tokens("4.5-2.0")
        expected = [
            (Token.FLOAT, "4.5"),
            (Token.MINUS, "-"),
            (Token.FLOAT, "2.0"),
        ]
        self.assertEqual(tokens, expected)

    def test_float_multiplication(self):
        tokens = self._tokens("1.5*2.0")
        expected = [
            (Token.FLOAT, "1.5"),
            (Token.ASTERISK, "*"),
            (Token.FLOAT, "2.0"),
        ]
        self.assertEqual(tokens, expected)

    def test_float_division(self):
        tokens = self._tokens("5.0/2.0")
        expected = [
            (Token.FLOAT, "5.0"),
            (Token.SLASH, "/"),
            (Token.FLOAT, "2.0"),
        ]
        self.assertEqual(tokens, expected)

    # ---------- Mixed int / float & negatives ----------

    def test_int_plus_float(self):
        tokens = self._tokens("1+2.5")
        expected = [
            (Token.INT, "1"),
            (Token.PLUS, "+"),
            (Token.FLOAT, "2.5"),
        ]
        self.assertEqual(tokens, expected)

    def test_float_plus_int(self):
        tokens = self._tokens("2.5+2")
        expected = [
            (Token.FLOAT, "2.5"),
            (Token.PLUS, "+"),
            (Token.INT, "2"),
        ]
        self.assertEqual(tokens, expected)

    def test_negative_int_and_plus(self):
        tokens = self._tokens("-1+2")
        expected = [
            (Token.INT, "-1"),
            (Token.PLUS, "+"),
            (Token.INT, "2"),
        ]
        self.assertEqual(tokens, expected)

    def test_negative_float_multiplication(self):
        tokens = self._tokens("-1.5*2")
        expected = [
            (Token.FLOAT, "-1.5"),
            (Token.ASTERISK, "*"),
            (Token.INT, "2"),
        ]
        self.assertEqual(tokens, expected)


if __name__ == "__main__":
    unittest.main()
