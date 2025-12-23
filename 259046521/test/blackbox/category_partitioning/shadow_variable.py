from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest


class ShadowVariableTester(unittest.TestCase):
    def test1(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("""
                let b = 0;
                fn thing(){
                    print(a);
                };
                thing();
            """)
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)

    def test2(self):
        with self.assertRaises(RuntimeEvaluationError):
            lexer: Lexer = Lexer("""
                let c = 0;
                fn thing(){
                    print(a);
                };
                thing();
            """)
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)

    def test3(self):
        try:
            lexer: Lexer = Lexer("""
                let a = 0;
                fn thing(){
                    print(a);
                };
                thing();
            """)
            parser = Parser(lexer)
            expressions = parser.run()
            evaluate(expressions)
        except Exception: # pragma: no cover
            self.fail("Test case 3 should not be throwing errors")


