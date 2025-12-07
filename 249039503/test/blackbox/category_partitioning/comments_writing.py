import unittest

from src.lexer import Lexer
from src.tokens import Token


class TestComments(unittest.TestCase):
    def _collect_tokens(self, source: str):
        lexer = Lexer(source)
        tokens = []

        tok, val = lexer.next_token()
        while tok is not Token.EOF:
            tokens.append((tok, val))
            tok, val = lexer.next_token()

        return tokens

    def test_hash_comment_only_line_newline(self):
        src = "# just a comment\n"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "Comment-only line should produce no tokens")

    def test_hash_comment_only_line_eof(self):
        src = "# just a comment"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "Comment-only at EOF should produce no tokens")

    def test_slashslash_comment_only_line_newline(self):
        src = "// just a comment\n"
        tokens = self._collect_tokens(src)

        self.assertEqual(tokens, [], "'//' Comment-only line should produce no tokens")

    def test_slashslash_comment_only_line_eof(self):
        src = "// just a comment"
        tokens = self._collect_tokens(src)

        self.assertEqual(
            tokens, [], "'//' Comment-only at EOF should produce no tokens"
        )

    def test_leading_comment_lines_before_code(self):
        src = "# first comment line\n# second comment line\nlet x = 1;"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_end_of_line_hash_comment_after_code(self):
        src = "let x = 1; # trailing comment\n"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_end_of_line_slashslash_comment_after_code(self):
        src = "let x = 1; // trailing comment\n"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_empty_hash_comment_line(self):
        src = "#\nlet x = 1"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_hash_comment_with_leading_spaces(self):
        src = "   # spaced comment\nlet x = 1"
        tokens = self._collect_tokens(src)

        expected_tokens = [
            (Token.LET, "let"),
            (Token.IDENTIFIER, "x"),
            (Token.ASSIGN, "="),
            (Token.INT, "1"),
        ]
        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()
