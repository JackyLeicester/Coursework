import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class NestMathOperationsBranchTest(unittest.TestCase):
    def test_simple_nested_add_mul(self):
        # 1 + (2 * 3) = 7
        self.assertEqual(run("1 + (2 * 3);"), 7)

    def test_deeply_nested_parentheses(self):
        # (((1 + 2) * 3) - 4) = 5
        self.assertEqual(run("(((1 + 2) * 3) - 4);"), 5)

    def test_nested_mixed_precedence(self):
        # (1 + 2) * (3 + 4) = 21
        self.assertEqual(run("(1 + 2) * (3 + 4);"), 21)

    def test_nested_unary_inside(self):
        self.assertEqual(run("-(2 * (3 + 1));"), 8)

    def test_unary_and_binary_chain(self):
        # -1 - (2 * -3) = -1 - (-6) = 5
        self.assertEqual(run("-1 - (2 * -3);"), 5)

    def test_nested_division_associativity(self):
        # (20 / (2 * 2)) = 5
        self.assertEqual(run("20 / (2 * 2);"), 5)

    def test_left_associative_without_parentheses(self):
        # ((10 - 3) - 2) = 5
        self.assertEqual(run("10 - 3 - 2;"), 5)

    def test_missing_closing_parenthesis_raises(self):
        with self.assertRaises(Exception):
            run("1 + (2 * (3 + 4);")

    def test_operator_after_open_paren_raises(self):
        with self.assertRaises(Exception):
            run("(+ 2);")
