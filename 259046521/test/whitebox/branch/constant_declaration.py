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
    # based on branch testing and ensuring all bran ches are tested
    def test1(self):
        output: str = run_test("const realname = 5;")
        self.assertEqual(output, "")

    def test2(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("const realname = 5; const realname = 3;")
            parser: Parser = Parser(lexer)
            statements = parser.run()
            evaluate(statements)

    def test3(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("const realname = 5; realname = 8;")
            parser: Parser = Parser(lexer)
            statements = parser.run()
            evaluate(statements)
