import unittest

from src.parser import Parser, IntegerLiteral, FloatLiteral, InfixExpression
from src.lexer import Lexer
from src.tokens import Token


class ComparativeOperatorsTest(unittest.TestCase):
    @staticmethod
    def parse_expression(src: str):
        lexer = Lexer(src)
        parser = Parser(lexer)
        return parser.parse_expression()

    def test_less_than(self):
        infix_expr = self.parse_expression("1 < 2")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.LESS)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_greater_than(self):
        infix_expr = self.parse_expression("2.1 > 1.2")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, FloatLiteral)
        self.assertEqual(infix_expr.operation, Token.GREATER)
        self.assertIsInstance(infix_expr.rhs, FloatLiteral)

    def test_less_than_or_equal_to(self):
        infix_expr = self.parse_expression("1 <= 1")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.LESSEQUAL)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_greater_than_or_equal_to(self):
        infix_expr = self.parse_expression("1 >= 1")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.GREATEREQUAL)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_equal_to(self):
        infix_expr = self.parse_expression("1 == 1")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.EQUAL)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_not_equal_to(self):
        infix_expr = self.parse_expression("1 != 2")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.NOTEQUAL)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_error_type_mismatch(self):
        lexer = Lexer("1 > 2.1")
        parser = Parser(lexer)
        self.assertRaises(Exception, parser.parse_expression)


if __name__ == "__main__":
    unittest.main()
