import unittest
from src.lexer import Lexer
from src.parser import (
    Parser,
    WhileStatement,
    InfixExpression,
    BlockStatement,
    IncorrectSyntax,
)


class TestWhileLoopProcessing(unittest.TestCase):
    @staticmethod
    def parse(src: str):
        lexer = Lexer(src)
        parser = Parser(lexer)
        return parser.run()

    def test_correct_while_loop_syntax(self):
        program = """
        let x = 0;
        while (x < 2) {
        }
        """
        expressions = self.parse(program)

        # Second expression should be while loop
        while_stmt = expressions[1]

        self.assertIsInstance(while_stmt, WhileStatement)
        self.assertIsInstance(while_stmt.condition, InfixExpression)
        self.assertIsInstance(while_stmt.block, BlockStatement)

    def test_wrong_while_loop_syntax(self):
        program = """
        let x = 0;
        while x < 2 {
        }
        """
        with self.assertRaises(IncorrectSyntax):
            self.parse(program)


if __name__ == "__main__":
    unittest.main()
