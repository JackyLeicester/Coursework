from src.parser import IncorrectSyntax
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


def run_test(test_input: str) -> str:
    # buffer: StringIO = capture_output()
    lexer: Lexer = Lexer(test_input)
    parser: Parser = Parser(lexer)
    parser.run()
    return ""


def expect_exception(tester: unittest.TestCase, test_input: str):
    with tester.assertRaises(IncorrectSyntax):
        lexer: Lexer = Lexer(test_input)
        parser: Parser = Parser(lexer)
        parser.run()


class CallExpressionTest(unittest.TestCase):
    # Each of these tests check what happens if an error is thrown if any element of the expression is different from what is expected
    # if closing parethesis is missing
    def test1(self):
        expect_exception(self, "AAA({")

    def test2(self):
        expect_exception(self, "AAA(}")

    # if semicolon is missing or wrong
    def test3(self):
        expect_exception(self, "AAA(),")

    def test4(self):
        expect_exception(self, "AAA()AAA")

    # test is a valid callexpression can be parsed
    def test5(self):
        output: str = run_test("AAA();")
        self.assertEqual(output, "")
