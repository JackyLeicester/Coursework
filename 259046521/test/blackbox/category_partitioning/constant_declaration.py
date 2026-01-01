from src.lexer import Lexer
from src.parser import Parser, IncorrectSyntax
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


def run_test(test_input: str) -> str:
    lexer: Lexer = Lexer(test_input)
    parser: Parser = Parser(lexer)
    parser.run()
    return ""


def expect_exception(tester: unittest.TestCase, test_input: str):
    with tester.assertRaises(IncorrectSyntax):
        lexer: Lexer = Lexer(test_input)
        parser: Parser = Parser(lexer)
        parser.run()


class ConstantDeclarationTest(unittest.TestCase):
    # Each of these tests check what happens if an error is thrown if any element of the expression is different from what is expected
    # if the identifier is wrong
    def test1(self):
        expect_exception(self, "const true")

    def test2(self):
        expect_exception(self, "const false")

    # if the equal sign is wrong
    def test3(self):
        expect_exception(self, "const real_name ?")

    def test4(self):
        expect_exception(self, "const real_name ==")

    # if the semicolon is missing
    def test5(self):
        expect_exception(self, "const real_name HAM")

    def test6(self):
        output: str = run_test("const realname = 5;")
        self.assertEqual(output, "")
