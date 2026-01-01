from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate
import unittest


def run_test(test_input: str) -> str:
    lexer: Lexer = Lexer(test_input)
    parser: Parser = Parser(lexer)
    parser.run()
    return ""


def expect_exception(tester: unittest.TestCase, test_input: str):
    with tester.assertRaises(Exception):
        lexer: Lexer = Lexer(test_input)
        parser: Parser = Parser(lexer)
        parser.run()


class VariableDeclarationTest(unittest.TestCase):
    # tests errors branches on the parser
    def test1(self):
        expect_exception(self, "let true")

    # tests the main branch for variables
    def test2(self):
        lexer: Lexer = Lexer("let realname = 5; realname = 12; return realname;")
        parser: Parser = Parser(lexer)
        statements = parser.run()
        self.assertEqual(evaluate(statements), 12)
