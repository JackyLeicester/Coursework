import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def eval_program(code: str):
    expressions = Parser(Lexer(code)).run()
    return evaluate(expressions)


class TestCommentsWritingStatement(unittest.TestCase):
    def test_line_comment_ignored(self):
        program = """
        let x = 1; // this is a comment
        x = x + 2; // another comment
        x;
        """
        self.assertEqual(eval_program(program), 3)

    def test_line_comment_at_start(self):
        program = """
        // comment before code
        1 + 2;
        """
        self.assertEqual(eval_program(program), 3)


if __name__ == "__main__":
    unittest.main()
