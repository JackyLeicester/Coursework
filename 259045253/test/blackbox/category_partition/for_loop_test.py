import unittest
from src.lexer import Lexer
from src.parser import (
    Parser,
    ForStatement,
    LetStatement,
    InfixExpression,
    AssignExpression,
    BlockStatement,
    IncorrectSyntax,
)


class TestForLoopProcessing(unittest.TestCase):
    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    def test_correct_for_loop_syntax(self):
        program = """
        for (let x = 1; x < 2; x = x + 1) {
            # Some statement
        }
        """
        parser = self.setup_parser(program)
        for_stmt = parser.parse_for_statement()

        self.assertIsInstance(for_stmt, ForStatement)
        self.assertIsInstance(for_stmt.initialization, LetStatement)
        self.assertIsInstance(for_stmt.condition, InfixExpression)
        self.assertIsInstance(for_stmt.increment, AssignExpression)
        self.assertIsInstance(for_stmt.block, BlockStatement)

    def test_wrong_for_loop_syntax(self):
        program = """
        for (let x = 1 x < 2; x = x + 1) {
            # Some statement
        }
        """
        parser = self.setup_parser(program)
        self.assertRaises(IncorrectSyntax, parser.parse_for_statement)


if __name__ == "__main__":
    unittest.main()
