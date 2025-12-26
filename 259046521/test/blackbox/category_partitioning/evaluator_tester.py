from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest

def run_test(input: str):
    lexer: Lexer = Lexer(input)
    parser: Parser = Parser(lexer)
    statements = parser.run()
    return evaluate(statements)

class FunctionTester(unittest.TestCase):
    def test1(self):
        self.assertEqual(run_test("return 5.0;"), 5.0)

    def test2(self):
        self.assertEqual(run_test("return \'a\';"), 'a')
    
    def test3(self):
        self.assertEqual(run_test("return sqrt(9);"), 3)

    def test4(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return sqrt(9, 5);")
    
    def test5(self):
        self.assertEqual(run_test("return pow(3, 2);"), 9)
    
    def test6(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return pow(3, 2, 4);")
    
    def test7(self):
        self.assertEqual(run_test("return ceil(1.3);"), 2)
    
    def test8(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return ceil();")
    
    def test9(self):
        self.assertEqual(run_test("return floor(1.3);"), 1)
    
    def test10(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return floor();")
    
    def test11(self):
        self.assertEqual(run_test("return abs(-5);"), 5)
    
    def test12(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return abs();")
    
    def test13(self):
        run_test("println(5);")
    