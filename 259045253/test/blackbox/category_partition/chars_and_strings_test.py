import unittest

from src import Parser, Lexer
from src.tokens import Token
from src.parser import StringLiteral, CharLiteral


class TestCharStrings(unittest.TestCase):
    @staticmethod
    def setup_lexer(src: str) -> Lexer:
        return Lexer(src)

    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        parser = Parser(lexer)
        return parser

    def test_empty_string(self):
        parser = self.setup_parser('""')
        string = parser.parse_expression()
        self.assertIsInstance(string, StringLiteral)
        self.assertEqual(string.literal, "")

    def test_some_string(self):
        some_string = "this is some string"
        parser = self.setup_parser(f'"{some_string}"')
        string = parser.parse_expression()
        self.assertIsInstance(string, StringLiteral)
        self.assertEqual(string.literal, some_string)

    def test_open_double_quote_only(self):
        lexer = self.setup_lexer('"')
        token, _ = lexer._read_char_string()
        self.assertEqual(token, Token.EOF)

    def test_empty_character(self):
        parser = self.setup_parser("''")
        char = parser.parse_expression()
        self.assertIsInstance(char, CharLiteral)
        self.assertEqual(char.literal, "")

    def test_some_character(self):
        parser = self.setup_parser("'A'")
        char = parser.parse_expression()
        self.assertIsInstance(char, CharLiteral)
        self.assertEqual(char.literal, "A")

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
