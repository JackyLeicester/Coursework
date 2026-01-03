from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


class IfExistsTest(unittest.TestCase):
    # since callexpressions have already been tested, we will only test invalid parameters
    # a valid expression
    def test1(self):
        lexer: Lexer = Lexer("""
            return ifExists("a");
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        self.assertFalse(evaluate(expressions))

    # testing invalid parameters
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

    # testing an outcome that would lead to true as the output
    def test4(self):
        lexer: Lexer = Lexer("""
            let a = 3;
            return ifExists("a");
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        evaluate(expressions)


if __name__ == "__main__":
    unittest.main()
