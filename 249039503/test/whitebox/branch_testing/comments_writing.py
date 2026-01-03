import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class CommentsWritingBranchTest(unittest.TestCase):
    def test_line_comment_1(self):
        code = """
        // full line comment
        1 + 2;
        """
        self.assertEqual(run(code), 3)

    def test_line_comment_after_expression_2(self):
        code = "1 + 2; // trailing comment"
        self.assertEqual(run(code), 3)

    def test_line_comment_after_statement_followed_by_new_statement_3(self):
        code = """
        1 + 2; // comment
        3;
        """
        self.assertEqual(run(code), 3)

    def test_comments_between_statements_4(self):
        code = """
        let x = 1;
        // mid
        let y = 2;
        // end
        x + y;
        """
        self.assertEqual(run(code), 3)

    def test_comment_markers_inside_string_not_comment_5(self):
        code = r"""
        let s = "not a // comment";
        1 + 2;
        """
        self.assertEqual(run(code), 3)
