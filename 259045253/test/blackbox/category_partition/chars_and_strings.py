import unittest
from src.lexer import Lexer
from src.tokens import Token


class TestStringProcessing(unittest.TestCase):
    @staticmethod
    def setup_lexer(src: str) -> Lexer:
        return Lexer(src)

    def test_empty_string(self):
        lexer = self.setup_lexer('""')
        token, str_repr = lexer._read_char_string()
        self.assertEqual(token, Token.STRING)
        self.assertEqual(str_repr, "")

    def test_some_string(self):
        some_string = "this is some string"
        lexer = self.setup_lexer(f'"{some_string}"')
        token, str_repr = lexer._read_char_string()
        self.assertEqual(token, Token.STRING)
        self.assertEqual(str_repr, some_string)

    def test_open_double_quote_only(self):
        lexer = self.setup_lexer('"')
        token, _ = lexer._read_char_string()
        self.assertEqual(token, Token.EOF)

    def test_empty_character(self):
        lexer = self.setup_lexer("''")
        token, str_repr = lexer._read_char_string()
        self.assertEqual(token, Token.CHAR)
        self.assertEqual(str_repr, "")

    def test_some_character(self):
        lexer = self.setup_lexer("'A'")
        token, str_repr = lexer._read_char_string()
        self.assertEqual(token, Token.CHAR)
        self.assertEqual(str_repr, "A")

    def test_open_single_quote_only(self):
        lexer = self.setup_lexer("'")
        token, _ = lexer._read_char_string()
        self.assertEqual(token, Token.EOF)

    def test_more_than_one_char_in_single_quote(self):
        lexer = self.setup_lexer("'foo'")
        token, _ = lexer._read_char_string()
        self.assertEqual(token, Token.EOF)


if __name__ == "__main__":
    unittest.main()
