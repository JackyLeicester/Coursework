from io import StringIO
from src.lexer import Lexer
from src.parser import Parser
import unittest
import sys


def capture_output():
    captured_output = StringIO()
    sys.stdout = captured_output


def stop_capture() -> str:
    if not hasattr(sys.stdout, "getvalue"):
        return ""
    output: str = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    return output


def run_test(test_input: str) -> str:
    capture_output()
    lexer: Lexer = Lexer(test_input)
    parser: Parser = Parser(lexer)
    parser.run()
    return stop_capture()


def expect_exception(tester: unittest.TestCase, test_input: str):
    with tester.assertRaises(Exception):
        lexer: Lexer = Lexer(test_input)
        parser: Parser = Parser(lexer)
        parser.run()


class VariableDeclarationTest(unittest.TestCase):
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
        output: str = run_test("let realname = 5")
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
