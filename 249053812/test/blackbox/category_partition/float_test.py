import unittest
from src.lexer import Lexer
from src.tokens import Token


class FloatTestHarness(unittest.TestCase):
    """
    Test harness for float declaration and parsing.
    Based on Category Partition specification: float_test.tsl

    Categories:
    - DeclarationStructure: Valid Let Assignment, Missing Let Keyword, Missing Variable Name, Missing Equals Sign
    - FloatFormat: Positive Decimal, Negative Decimal, Zero Value, Integer Value, Trailing Dot, Non Numeric
    - Terminator: Semicolon Present, Semicolon Missing
    """

    def _collect_tokens(self, source: str):
        """Helper: collect all tokens from source code"""
        lexer = Lexer(source)
        tokens = []
        token, val = lexer.next_token()
        while token != Token.EOF:
            tokens.append((token, val))
            token, val = lexer.next_token()
        return tokens

    # Error Cases (Test Cases 1-5)

    def test_error_missing_let_keyword(self):
        """Test Case 1: DeclarationStructure = Missing Let Keyword [error]"""
        src = "x = 3.14;"
        tokens = self._collect_tokens(src)
        # Should not start with LET token
        self.assertNotEqual(tokens[0][0], Token.LET)
        # Should still parse identifier and assignment
        self.assertIn(Token.IDENTIFIER, [t[0] for t in tokens])

    def test_error_missing_variable_name(self):
        """Test Case 2: DeclarationStructure = Missing Variable Name [error]"""
        src = "let = 3.14;"
        tokens = self._collect_tokens(src)
        # After LET, should see ASSIGN instead of IDENTIFIER
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[1][0], Token.ASSIGN)

    def test_error_missing_equals_sign(self):
        """Test Case 3: DeclarationStructure = Missing Equals Sign [error]"""
        src = "let x 3.14;"
        tokens = self._collect_tokens(src)
        # Should have LET and IDENTIFIER but no ASSIGN before FLOAT
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[1][0], Token.IDENTIFIER)
        self.assertEqual(tokens[2][0], Token.FLOAT)

    def test_error_trailing_dot_float(self):
        """Test Case 4: FloatFormat = Trailing Dot [error]"""
        # Lexer should raise exception for trailing dot
        src = "let x = 5.;"
        try:
            lexer = Lexer(src)
            token, val = lexer.next_token()
            while token != Token.EOF:
                token, val = lexer.next_token()
            self.fail("Expected exception for trailing dot in float")
        except Exception as e:
            self.assertIn("Wrong declaration of float", str(e))

    def test_error_non_numeric_value(self):
        """Test Case 5: FloatFormat = Non Numeric [error]"""
        src = "let x = abc;"
        tokens = self._collect_tokens(src)
        # 'abc' should be parsed as IDENTIFIER, not FLOAT
        token_types = [t[0] for t in tokens]
        self.assertNotIn(Token.FLOAT, token_types)
        # Should have an IDENTIFIER for 'abc'
        identifiers = [t[1] for t in tokens if t[0] == Token.IDENTIFIER]
        self.assertIn("abc", identifiers)

    # Valid Cases with Semicolon (Test Cases 6, 8, 10, 12)

    def test_valid_positive_decimal_with_semicolon(self):
        """Test Case 6 (Key=1.1.1): Valid Let Assignment + Positive Decimal + Semicolon Present"""
        src = "let x = 3.14;"
        tokens = self._collect_tokens(src)
        self.assertEqual(len(tokens), 5)  # let, x, =, 3.14, ;
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[1][0], Token.IDENTIFIER)
        self.assertEqual(tokens[1][1], "x")
        self.assertEqual(tokens[2][0], Token.ASSIGN)
        self.assertEqual(tokens[3][0], Token.FLOAT)
        self.assertEqual(tokens[3][1], "3.14")
        self.assertEqual(tokens[4][0], Token.SEMICOLON)

    def test_valid_negative_decimal_with_semicolon(self):
        """Test Case 8 (Key=1.2.1): Valid Let Assignment + Negative Decimal + Semicolon Present"""
        src = "let y = -2.71828;"
        tokens = self._collect_tokens(src)
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[1][0], Token.IDENTIFIER)
        self.assertEqual(tokens[1][1], "y")
        self.assertEqual(tokens[2][0], Token.ASSIGN)
        self.assertEqual(tokens[3][0], Token.FLOAT)
        self.assertEqual(tokens[3][1], "-2.71828")
        self.assertEqual(tokens[4][0], Token.SEMICOLON)

    def test_valid_zero_value_with_semicolon(self):
        """Test Case 10 (Key=1.3.1): Valid Let Assignment + Zero Value + Semicolon Present"""
        src = "let z = 0.0;"
        tokens = self._collect_tokens(src)
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[3][0], Token.FLOAT)
        self.assertEqual(tokens[3][1], "0.0")
        self.assertEqual(tokens[4][0], Token.SEMICOLON)

    def test_valid_integer_value_with_semicolon(self):
        """Test Case 12 (Key=1.4.1): Valid Let Assignment + Integer Value + Semicolon Present"""
        src = "let count = 5;"
        tokens = self._collect_tokens(src)
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[1][0], Token.IDENTIFIER)
        self.assertEqual(tokens[2][0], Token.ASSIGN)
        self.assertEqual(tokens[3][0], Token.INT)
        self.assertEqual(tokens[3][1], "5")
        self.assertEqual(tokens[4][0], Token.SEMICOLON)

    # Valid Cases without Semicolon (Test Cases 7, 9, 11, 13)

    def test_valid_positive_decimal_no_semicolon(self):
        """Test Case 7 (Key=1.1.2): Valid Let Assignment + Positive Decimal + Semicolon Missing"""
        src = "let x = 3.14"
        tokens = self._collect_tokens(src)
        self.assertEqual(len(tokens), 4)  # let, x, =, 3.14 (no semicolon)
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[3][0], Token.FLOAT)
        # No semicolon at end
        self.assertNotEqual(tokens[-1][0], Token.SEMICOLON)

    def test_valid_negative_decimal_no_semicolon(self):
        """Test Case 9 (Key=1.2.2): Valid Let Assignment + Negative Decimal + Semicolon Missing"""
        src = "let y = -2.71828"
        tokens = self._collect_tokens(src)
        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0][0], Token.LET)
        self.assertEqual(tokens[3][0], Token.FLOAT)
        self.assertNotEqual(tokens[-1][0], Token.SEMICOLON)

    def test_valid_zero_value_no_semicolon(self):
        """Test Case 11 (Key=1.3.2): Valid Let Assignment + Zero Value + Semicolon Missing"""
        src = "let z = 0.0"
        tokens = self._collect_tokens(src)
        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[3][0], Token.FLOAT)

    def test_valid_integer_value_no_semicolon(self):
        """Test Case 13 (Key=1.4.2): Valid Let Assignment + Integer Value + Semicolon Missing"""
        src = "let count = 5"
        tokens = self._collect_tokens(src)
        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[3][0], Token.INT)


if __name__ == "__main__":
    unittest.main()
