import unittest

from src import Parser, Lexer, evaluate
from src.parser import NullLiteral


class LogicalOperatorsTest(unittest.TestCase):
    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    def test_null(self):
        parser = self.setup_parser("null")
        null = parser.parse_null()
        self.assertIsInstance(null, NullLiteral)

    def test_null_evaluation(self):
        parser = self.setup_parser("null")
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()
