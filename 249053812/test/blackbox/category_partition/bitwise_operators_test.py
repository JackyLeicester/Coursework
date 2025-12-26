import unittest
from src.parser import Parser, IntegerLiteral, InfixExpression, IncorrectSyntax
from src.lexer import Lexer
from src.tokens import Token
from src.evaluator import RuntimeEvaluationError


# PART 1: Parser Tests (Checking AST Structure)
class BitwiseParserTest(unittest.TestCase):
    @staticmethod
    def parse_expression(src: str):
        lexer = Lexer(src)
        parser = Parser(lexer)
        return parser.parse_expression()

    def test_bitwise_and_structure(self):
        """Test that '1 & 2' parses into an InfixExpression with BITWISE_AND"""
        infix_expr = self.parse_expression("1 & 2")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.BITWISE_AND)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_bitwise_or_structure(self):
        """Test that '3 | 4' parses into an InfixExpression with BITWISE_OR"""
        infix_expr = self.parse_expression("3 | 4")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.BITWISE_OR)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_bitwise_xor_structure(self):
        """Test that '5 ^ 6' parses into an InfixExpression with BITWISE_XOR"""
        infix_expr = self.parse_expression("5 ^ 6")
        self.assertIsInstance(infix_expr, InfixExpression)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)
        self.assertEqual(infix_expr.operation, Token.BITWISE_XOR)
        self.assertIsInstance(infix_expr.rhs, IntegerLiteral)

    def test_precedence_mixed(self):
        """
        Verify Precedence: 1 | 2 & 3
        Based on your parser.py, AND (5) > OR (3).
        Should parse as: 1 | (2 & 3)
        """
        infix_expr = self.parse_expression("1 | 2 & 3")
        # Top level should be OR
        self.assertEqual(infix_expr.operation, Token.BITWISE_OR)
        self.assertIsInstance(infix_expr.lhs, IntegerLiteral)  # 1

        # Right side should be the AND expression
        self.assertIsInstance(infix_expr.rhs, InfixExpression)
        self.assertEqual(infix_expr.rhs.operation, Token.BITWISE_AND)


# PART 2: Evaluator Tests (Checking Logic & Errors)
# This satisfies your TSL requirements for "Return: Integer" and "Error: Incorrect Argument Type"
class BitwiseEvaluatorTest(unittest.TestCase):
    def _evaluate(self, src: str):
        """Helper to run the full interpreter pipeline"""
        lexer = Lexer(src)
        parser = Parser(lexer)
        expressions = parser.run()
        # Return the result of the first expression
        from src.evaluator import _eval

        return _eval(expressions[0].expression, {})

    # TSL: Arguments = Valid Integers
    def test_eval_bitwise_and(self):
        # 6 (110) & 3 (011) = 2 (010)
        self.assertEqual(self._evaluate("6 & 3;"), 2)

    def test_eval_bitwise_or(self):
        # 6 (110) | 3 (011) = 7 (111)
        self.assertEqual(self._evaluate("6 | 3;"), 7)

    def test_eval_bitwise_xor(self):
        # 6 (110) ^ 3 (011) = 5 (101)
        self.assertEqual(self._evaluate("6 ^ 3;"), 5)

    # TSL: Arguments = Incorrect Argument Type [error]
    def test_error_float_type(self):
        """Ensures logic rejects floats"""
        with self.assertRaises(RuntimeEvaluationError) as cm:
            self._evaluate("6 & 3.5;")
        self.assertIn("Bitwise operations require integers", str(cm.exception))

    # TSL: Arguments = Missing Comma (Syntax Error context)
    def test_error_syntax_malformed(self):
        """Ensures parser catches bad syntax like '6 & ;'"""
        lexer = Lexer("6 & ;")
        parser = Parser(lexer)
        with self.assertRaises(IncorrectSyntax):
            parser.run()


if __name__ == "__main__":
    unittest.main()
