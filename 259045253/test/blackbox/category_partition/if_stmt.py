import unittest

from src.lexer import Lexer
from src.parser import (
    Parser,
    IfExpression,
    BooleanLiteral,
    BlockStatement,
    InfixExpression,
)


class TestIfStatement(unittest.TestCase):
    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    def test_missing_block_statement(self):
        src = """
        if x < 1
        """
        parser = self.setup_parser(src)
        self.assertRaises(Exception, parser.parse_if_expression)

    def test_correct_if_syntax_literal(self):
        src = """
        if true {
            # some statements
        }
        """
        parser = self.setup_parser(src)
        if_stmt = parser.parse_if_expression()
        self.assertIsInstance(if_stmt, IfExpression)
        self.assertIsInstance(if_stmt.condition, BooleanLiteral)
        self.assertIsInstance(if_stmt.consequence, BlockStatement)
        self.assertEqual(if_stmt.alternative, None)

    def test_missing_else_block(self):
        src = """
        if true {
            # some statements
        } else
        """
        parser = self.setup_parser(src)
        self.assertRaises(Exception, parser.parse_if_expression)

    def test_correct_if_syntax_expression(self):
        src = """
        if x < 2 {
            # some statements
        }
        """
        parser = self.setup_parser(src)
        if_stmt = parser.parse_if_expression()
        self.assertIsInstance(if_stmt, IfExpression)
        self.assertIsInstance(if_stmt.condition, InfixExpression)
        self.assertIsInstance(if_stmt.consequence, BlockStatement)
        self.assertEqual(if_stmt.alternative, None)

    def test_else_keyword_present(self):
        src = """
        if true {
            # some statements
        } else {
            # some more statements
        }
        """
        parser = self.setup_parser(src)
        if_stmt = parser.parse_if_expression()
        self.assertIsInstance(if_stmt, IfExpression)
        self.assertIsInstance(if_stmt.condition, BooleanLiteral)
        self.assertIsInstance(if_stmt.consequence, BlockStatement)
        self.assertIsInstance(if_stmt.alternative, BlockStatement)


if __name__ == "__main__":
    unittest.main()
