import unittest

from src import Lexer, Parser, evaluate
from src.parser import ContinueStatement
from src.evaluator import RuntimeEvaluationError
from src.tokens import Token


class TestContinueStmt(unittest.TestCase):
    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    # Test 1: case "continue"
    def test_lexer1(self):
        lexer = Lexer("continue")
        (token, _str_repr) = lexer.next_token()
        self.assertEqual(token, Token.CONTINUE)

    # Test 1: `parse_continue_statement` method
    def test_parser1(self):
        parser = self.setup_parser("continue;")
        char = parser.parse_continue_statement()
        self.assertIsInstance(char, ContinueStatement)

    # Test 1: `ContinueStatement` handling in `evaluate` function
    def test_evaluator1(self):
        parser = self.setup_parser("continue;")
        expressions = parser.run()
        self.assertRaises(RuntimeEvaluationError, evaluate, expressions)

    # Test 2: `ContinueStatement` handling in `evaluate` function
    def test_evaluator2(self):
        parser = self.setup_parser("""
        for (let x = 1; x < 1; x = x + 1) {
            continue;
        }
        """)
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()
