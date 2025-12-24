from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate
import unittest


def run_test(test_input: str) -> str:
    # buffer: StringIO = capture_output()
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
    # based on category partition
    def test1(self):
        expect_exception(self, "let true")

    def test2(self):
        expect_exception(self, "let false")

    def test3(self):
        expect_exception(self, "let true")

    def test4(self):
        expect_exception(self, "let real_name ?")

    def test5(self):
        expect_exception(self, "let real_name ==")

    def test6(self):
        expect_exception(self, "let real_name HAM")

    def test7(self):
        output: str = run_test("let realname = 5;")
        self.assertEqual(output, "")

    # based on branch testing
    def test8(self):
        lexer: Lexer = Lexer("let realname = 5; realname = 12;")
        parser: Parser = Parser(lexer)
        statements = parser.run()
        evaluate(statements)
