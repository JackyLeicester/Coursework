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
    # based on category partition, testing code inputs
    def test1(self):
        expect_exception(self, "const true")

    def test2(self):
        expect_exception(self, "const false")

    def test3(self):
        expect_exception(self, "const true")

    def test4(self):
        expect_exception(self, "const real_name ?")

    def test5(self):
        expect_exception(self, "const real_name ==")

    def test6(self):
        expect_exception(self, "const real_name HAM")

    def test7(self):
        output: str = run_test("const realname = 5;")
        self.assertEqual(output, "")

    # based on branch testing and ensuring all bran ches are tested

    def test8(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("const realname = 5; const realname = 3;")
            parser: Parser = Parser(lexer)
            statements = parser.run()
            evaluate(statements)

    def test9(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("const realname = 5; realname = 8;")
            parser: Parser = Parser(lexer)
            statements = parser.run()
            evaluate(statements)
