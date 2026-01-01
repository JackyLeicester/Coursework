import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class LogicalErrorBranchTest(unittest.TestCase):
    # --- arithmetic correctness branches ---
    def test_division_basic(self):
        self.assertEqual(run("10 / 2;"), 5)

    def test_division_left_associative(self):
        # (20/2)/2 = 5 (not 20/(2/2)=20)
        self.assertEqual(run("20 / 2 / 2;"), 5)

    def test_precedence_mul_before_add(self):
        self.assertEqual(run("1 + 2 * 3;"), 7)

    def test_parentheses_override_precedence(self):
        self.assertEqual(run("(1 + 2) * 3;"), 9)

    def test_nested_parentheses(self):
        self.assertEqual(run("((1 + 2) * (3 + 4));"), 21)

    # --- runtime error branches ---
    def test_division_by_zero_raises(self):
        with self.assertRaises(Exception):
            run("10 / 0;")

    def test_undefined_variable_raises(self):
        with self.assertRaises(Exception) as ctx:
            run("x;")
        # accept both message variants
        msg = str(ctx.exception)
        self.assertTrue(("Undefined variable" in msg) or ("Undefined" in msg))

    # --- parser/syntax error branches ---
    def test_missing_closing_parenthesis_raises(self):
        with self.assertRaises(Exception):
            run("1 + (2 * (3 + 4);")

    def test_operator_missing_rhs_raises(self):
        with self.assertRaises(Exception):
            run("1 + ;")
