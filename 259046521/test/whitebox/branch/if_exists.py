from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


class ReturnErrorCodeTest(unittest.TestCase):
    def test1(self):
        lexer: Lexer = Lexer("""
            return ifExists("a");
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        evaluate(expressions)

    def test2(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("""
                return ifExists(true);""")
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)

    def test3(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("""
                return ifExists(5);""")
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)

    def test4(self):
        lexer: Lexer = Lexer("""
            let a = 3;
            return ifExists("a");
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        evaluate(expressions)
