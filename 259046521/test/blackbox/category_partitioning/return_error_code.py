from src.lexer import Lexer
from src.parser import Parser, IncorrectSyntax
from src.evaluator import evaluate
import unittest


class ReturnErrorCodeTest(unittest.TestCase):
    def test1(self):
        with self.assertRaises(IncorrectSyntax):
            lexer: Lexer = Lexer("return let a = 3;")
            parser = Parser(lexer)
            parser.run()

    def test2(self):
        with self.assertRaises(IncorrectSyntax):
            lexer: Lexer = Lexer("return const b = 2;")
            parser = Parser(lexer)
            parser.run()

    def test3(self):
        lexer: Lexer = Lexer("return 5;")
        parser = Parser(lexer)
        expressions = parser.run()
        self.assertEqual(evaluate(expressions), "User error code: 5")
