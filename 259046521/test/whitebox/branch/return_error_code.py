from src.lexer import Lexer
from src.parser import Parser, IncorrectSyntax
from src.evaluator import evaluate
import unittest


class ReturnErrorCodeTest(unittest.TestCase):
    # reach an invalid branch in parser
    def test1(self):
        with self.assertRaises(IncorrectSyntax):
            lexer: Lexer = Lexer("return let a = 3;")
            parser = Parser(lexer)
            parser.run()
    # tests the valid branch up to evaluator
    def test2(self):
        lexer: Lexer = Lexer("return 5;")
        parser = Parser(lexer)
        expressions = parser.run()
        self.assertEqual(evaluate(expressions), 5)

