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

    def test_zero_1(self):
        src = "0"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "0")]
        self.assertEqual(tokens, expected)

    def test_positive_digit_2(self):
        src = "7"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "7")]
        self.assertEqual(tokens, expected)

    def test_positive_multi_digit_3(self):
        src = "567"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "567")]
        self.assertEqual(tokens, expected)

    def test_negative_single_digit_4(self):
        src = "-3"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "-3")]
        self.assertEqual(tokens, expected)

    def test_negative_multi_digit_5(self):
        src = "-857"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "-857")]
        self.assertEqual(tokens, expected)

    def test_leading_zero_integer_6(self):
        src = "007"
        tokens = self._collect_tokens(src)
        expected = [(Token.INT, "007")]
        self.assertEqual(tokens, expected)

    def test_assigned_positive_integer_7(self):
        src = "let x = 87"
        tokens = self._collect_tokens(src)
        expected = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "87"),
        ]
        self.assertEqual(tokens, expected)

    def test_assigned_negative_integer_8(self):
        src = "let x = -42"
        tokens = self._collect_tokens(src)
        expected = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "-42"),
        ]
        self.assertEqual(tokens, expected)

    def test_trailing_dot_error_9(self):
        src = "1."
        with self.assertRaises(Exception):
            self._collect_tokens(src)


if __name__ == "__main__":
    unittest.main()
