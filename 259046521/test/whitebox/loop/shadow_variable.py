from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest

# we cannot test the scenario with 0 loop iterations as there will always at least be 1 context
class Tester(unittest.TestCase):
    # loop more than once
    def test1(self):
        lexer: Lexer = Lexer("""
            let a = 2;
            fn thing(){
                let a = 0;
            };
            thing();
            return a;
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        self.assertEqual(evaluate(expressions), 2)
         
    # loop exactly once
    def test2(self):
        lexer: Lexer = Lexer("""
            let a = 0;
            fn thing(){
                let a = 2;
                a = 3;
            };
            thing();
            return a;
        """)
        parser = Parser(lexer)
        expressions = parser.run()
        self.assertEqual(evaluate(expressions), 0)
        