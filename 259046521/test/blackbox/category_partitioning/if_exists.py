from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import _is_declared, evaluate, RuntimeEvaluationError
import unittest


class ReturnErrorCodeTest(unittest.TestCase):
    def test1(self):
        lexer: Lexer = Lexer("""
            return ifExists("a");
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        self.assertEqual(evaluate(expressions), "User error code: False")


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

if __name__ == "__main__":
    unittest.main()
       