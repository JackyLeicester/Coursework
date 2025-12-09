import unittest

from src.parser import Parser, InfixExpression, BooleanLiteral, PrefixExpression
from src.lexer import Lexer
from src.tokens import Token


class LogicalOperatorsTest(unittest.TestCase):
    @staticmethod
    def parse_expression(src: str):
        lexer = Lexer(src)
        parser = Parser(lexer)
        return parser.parse_expression()

    def test_and(self):
        infix_expr = self.parse_expression("true && true")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, BooleanLiteral)
        self.assertEqual(infix_expr.operation, Token.AND)
        self.assertIsInstance(infix_expr.rhs, BooleanLiteral)

    def test_or(self):
        infix_expr = self.parse_expression("true || true")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, BooleanLiteral)
        self.assertEqual(infix_expr.operation, Token.OR)
        self.assertIsInstance(infix_expr.rhs, BooleanLiteral)

    def test_not(self):
        infix_expr = self.parse_expression("!true && true")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, PrefixExpression)
        self.assertIsInstance(infix_expr.lhs.right, BooleanLiteral)
        self.assertEqual(infix_expr.operation, Token.AND)
        self.assertIsInstance(infix_expr.rhs, BooleanLiteral)


if __name__ == "__main__":
    unittest.main()
