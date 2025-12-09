import unittest

from src.lexer import Lexer
from src.tokens import Token


class IntegersTest(unittest.TestCase):
    def _collect_tokens(self, source: str):
        lexer = Lexer(source)
        tokens = []

        tok, val = lexer.next_token()
        while tok is not Token.EOF:
            tokens.append((tok, val))
            tok, val = lexer.next_token()

        return tokens

    def test_zero_standalone(self):
        src = "0"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "0")]
        self.assertEqual(tokens, expected)

    def test_positive_single_digit(self):
        src = "5"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "5")]
        self.assertEqual(tokens, expected)

    def test_positive_multi_digit(self):
        src = "123"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "123")]
        self.assertEqual(tokens, expected)

    def test_negative_single_digit(self):
        src = "-5"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "-5")]
        self.assertEqual(tokens, expected)

    def test_negative_multi_digit(self):
        src = "-123"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "-123")]
        self.assertEqual(tokens, expected)

    def test_leading_zero_integer(self):
        src = "007"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "007")]
        self.assertEqual(tokens, expected)

    def test_assignment_positive_integer(self):
        src = "let x = 42"
        tokens = self._collect_tokens(src)
        expected = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "42"),
        ]
        self.assertEqual(tokens, expected)

    def test_assignment_negative_integer(self):
        src = "let x = -42"
        tokens = self._collect_tokens(src)
        expected = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "-42"),
        ]
        self.assertEqual(tokens, expected)

    def test_trailing_dot_raises_error(self):
        src = "1."
        with self.assertRaises(Exception):
            self._collect_tokens(src)


if __name__ == "__main__":
    unittest.main()
