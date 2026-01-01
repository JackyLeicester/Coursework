from src.lexer import Lexer
from src.parser import Parser, IncorrectSyntax
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


class InputTest(unittest.TestCase):
    # similar to if_exists, less tests are necessary as
    def test1(self):
        with self.assertRaises(IncorrectSyntax):
            lexer: Lexer = Lexer("input(let a = 3);")
            parser = Parser(lexer)
            parser.run()

    def test2(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("input(5);")
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)


if __name__ == "__main__":
    unittest.main()
