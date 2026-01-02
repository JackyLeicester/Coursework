import unittest

from src import Lexer, Parser, evaluate
from src.parser import ForStatement
from src.tokens import Token


class TestForLoop(unittest.TestCase):

    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    # Test 1: case "for"
    def test_lexer1(self):
        lexer = Lexer("""
        for (let x = 1; x < 2; x = x + 1) {
            # Some statement
        }
        """)
        (token, _str_repr) = lexer.next_token()
        self.assertEqual(token, Token.FOR)

    # Test 1: `parse_for_statement` method
    def test_parser1(self):
        parser = self.setup_parser("""
        for (let x = 1; x < 2; x = x + 1) {
            # Some statement
        }
        """)
        char = parser.parse_for_statement()
        self.assertIsInstance(char, ForStatement)

    # Test 1: `ForStatement` handling in `evaluate` function
    def test_evaluator1(self):
        parser = self.setup_parser("""
        for (let x = 1; x < 2; x = x + 1) {
            # Some statement
        }
        """)
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(None, result)

    # Test 2: `ForStatement` handling in `evaluate` function, with `break`
    # and `continue` statements
    def test_evaluator2(self):
        parser = self.setup_parser("""
        for (let x = 1; x < 3; x = x + 1) {
            if x == 1 {
                continue;
            } else {
                break;
            }
        }
        """)
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()