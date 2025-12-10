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

    def test1(self):
        src = "# just a comment\n"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "Comment only line should produce no tokens")

    def test2(self):
        src = "# just a comment"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "Comment only at EOF should produce no tokens")

    def test3(self):
        src = "// just a comment\n"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "'//' Comment only line should produce no tokens")

    def test4(self):
        src = "// just a comment"
        tokens = self._collect_tokens(src)

        self.assertEqual(
            tokens, [], "'//' Comment only at EOF should produce no tokens"
        )

    def test5(self):
        src = "# first comment line\n# second comment line\nlet x = 1;"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
            (Token.SEMICOLON, ";"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test6(self):
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

    def test7(self):
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

    def test8(self):
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

    def test9(self):
        src = "   # spaced comment\nlet x = 1;"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
            (Token.SEMICOLON, ";")
        ]
        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()
