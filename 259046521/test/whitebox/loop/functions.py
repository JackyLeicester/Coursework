from src.parser import Parser
from src.lexer import Lexer
from src.evaluator import evaluate
import unittest


def run_test(input: str):
    lexer: Lexer = Lexer(input)
    parser: Parser = Parser(lexer)
    statements = parser.run()
    return evaluate(statements)


class Functions(unittest.TestCase):
    def test1(self):
        output = run_test("""
            fn thing(a, b, c){
                return a + b + c;
            };
            return thing(1, 2, 3);
        """)
        self.assertEqual(output, 6)

    def test2(self):
        output = run_test("""
            fn thing(){
                return 5;
            };
            return thing();
        """)
        self.assertEqual(output, 5)

    def test3(self):
        output = run_test("""
            fn thing(a){
                return a;
            };
            return thing(5);
        """)
        self.assertEqual(output, 5)
