import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def eval_program(code: str):
    expressions = Parser(Lexer(code)).run()
    return evaluate(expressions)


class TestCommentsCondition(unittest.TestCase):
    def test_line_comment_ignored(self):
        program = """
        // this is a comment
        1 + 2;
        """
        self.assertEqual(eval_program(program), 3)

    def test_inline_line_comment_ignored(self):
        program = "1 + 2; // comment here"
        self.assertEqual(eval_program(program), 3)

    def test_only_comment_program(self):
        program = "// only comment"
        self.assertIsNone(eval_program(program))


if __name__ == "__main__":
    unittest.main()
