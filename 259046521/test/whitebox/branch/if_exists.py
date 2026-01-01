from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


class ReturnErrorCodeTest(unittest.TestCase):
    # tests to ensure that the path leading to true and the path to false are both tested
    def test1(self):
        lexer: Lexer = Lexer("""
            return ifExists("a");
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        evaluate(expressions)

    def test2(self):
        lexer: Lexer = Lexer("""
            let a = 3;
            return ifExists("a");
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        evaluate(expressions)
