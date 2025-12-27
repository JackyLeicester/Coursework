from src.lexer import Lexer
from src.parser import Parser
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


class ReturnTest(unittest.TestCase):
    def test1(self):
        expect_exception(self, "return fn")

    def test2(self):
        expect_exception(self, "return let")

    def test3(self):
        output: str = run_test("return 5;")
        self.assertEqual(output, "")
