import unittest

from src import Parser, Lexer
from src.parser import ContinueStatement


class TestContinueStatement(unittest.TestCase):
    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    def test_missing_semicolon(self):
        parser = self.setup_parser("continue")
        self.assertRaises(Exception, parser.parse_continue_statement)

    def test_correct_syntax(self):
        parser = self.setup_parser("continue;")
        continue_stmt = parser.parse_continue_statement()
        self.assertIsInstance(continue_stmt, ContinueStatement)

    def test_wrong_keyword(self):
        parser = self.setup_parser("contineu;")
        self.assertRaises(Exception, parser.parse_continue_statement)


if __name__ == "__main__":
    unittest.main()
