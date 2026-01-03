import unittest

from src.lexer import Lexer
from src.tokens import Token


class CommentsTest(unittest.TestCase):
    def _collect_tokens(self, source: str):
        lexer = Lexer(source)
        tokens = []

        tok, val = lexer.next_token()
        while tok is not Token.EOF:
            tokens.append((tok, val))
            tok, val = lexer.next_token()

        return tokens

    def test_comment_line_1(self):
        src = "# just a comment\n"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "only no tokens")

    def test_comment_EOF_2(self):
        src = "# just a comment"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "only at EOF should produce no tokens")

    def test_only_1st_line_3(self):
        src = "# 1st comment line\n# 2nd comment line\nlet x = 1;"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
            (Token.SEMICOLON, ";"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_trailing_comment_4(self):
        src = "let x = 1; # trailing comment\n"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
            (Token.SEMICOLON, ";"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_trailing_comment_5(self):
        src = "let x = 1; // trailing comment\n"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
            (Token.SEMICOLON, ";"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_comment_6(self):
        src = "#\nlet x = 1;"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
            (Token.SEMICOLON, ";"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_spaced_comment_7(self):
        src = "   # spaced comment\nlet x = 1;"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
            (Token.SEMICOLON, ";"),
        ]
        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()
