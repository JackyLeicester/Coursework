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
    # tests the correct enforcement of syntax for variable declarations
    # wrong identifiers
    def test1(self):
        expect_exception(self, "let true")

    def test2(self):
        expect_exception(self, "let false")

    # missing assignment operator
    def test3(self):
        expect_exception(self, "let real_name ?")

    def test4(self):
        expect_exception(self, "let real_name ==")

    def test5(self):
        expect_exception(self, "let real_name HAM")

    # correct version of the program
    def test6(self):
        output: str = run_test("let realname = 5;")
        self.assertEqual(output, "")
