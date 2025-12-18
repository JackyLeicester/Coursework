from src.lexer import Lexer
from src.parser import Parser, IncorrectSyntax
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


class InputTest(unittest.TestCase):
    def test1(self):
        with self.assertRaises(IncorrectSyntax):
            lexer: Lexer = Lexer("input(let a = 3);")
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)

    def test2(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer('input("Enough", "Too much");')
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)
