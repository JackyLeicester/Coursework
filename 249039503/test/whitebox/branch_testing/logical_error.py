import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class LogicalErrorBranchTest(unittest.TestCase):
    # arithmetic correctness branches
    def test_division_basic_1(self):
        self.assertEqual(run("10 / 2;"), 5)

    def test_division_left_associative_2(self):
        self.assertEqual(run("20 / 2 / 2;"), 5)

    def test_precedence_mul_before_add_3(self):
        self.assertEqual(run("1 + 2 * 3;"), 7)

    def test_parentheses_override_precedence_4(self):
        self.assertEqual(run("(1 + 2) * 3;"), 9)

    def test_nested_parentheses_4(self):
        self.assertEqual(run("((1 + 2) * (3 + 4));"), 21)

    # runtime error branches
    def test_division_by_zero_raises_5(self):
        with self.assertRaises(Exception):
            run("10 / 0;")

    def test_undefined_variable_raises_6(self):
        with self.assertRaises(Exception) as ctx:
            run("x;")
        msg = str(ctx.exception)
        self.assertTrue(("Undefined variable" in msg) or ("Undefined" in msg))

    # parser/syntax error branches
    def test_missing_closing_parenthesis_raises_7(self):
        with self.assertRaises(Exception):
            run("1 + (2 * (3 + 4);")

    def test_operator_missing_rhs_raises_8(self):
        with self.assertRaises(Exception):
            run("1 + ;")
