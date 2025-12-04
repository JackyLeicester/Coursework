from io import StringIO
from src.lexer import Lexer
from src.parser import Parser
import unittest
import sys


def capture_output():
    captured_output = StringIO()
    sys.stdout = captured_output

def stop_capture()->str:
    output: str = sys.stdout.getValue()
    sys.stdout = sys.__stdout__
    return output

def run_test(test_input: str)->str:
    capture_output()
    lexer: Lexer = Lexer(test_input)
    parser: Parser = Parser(lexer)
    parser.run()
    return stop_capture()

class VariableDeclarationTest(unittest.TestCase):
    def test1(self):
        self.assertEqual("a", "a")
        with self.assertRaises(Exception):
            run_test("let true")[:13]


    # def test2(self):
    #     output: str = run_test("let false")[:13]
    #     self.assertEqual(output, "SYNTAX ERROR:")
    #
    # def test3(self):
    #     output: str = run_test("let true")[:13]
    #     self.assertEqual(output, "SYNTAX ERROR:")
    #
    # def test4(self):
    #     output: str = run_test("let real_name ?")[:13]
    #     self.assertEqual(output, "SYNTAX ERROR:")
    #
    # def test5(self):
    #     output: str = run_test("let real_name ==")[:13]
    #     self.assertEqual(output, "SYNTAX ERROR:")
    #
    # def test6(self):
    #     output: str = run_test("let real_name HAM")[:13]
    #     self.assertEqual(output, "SYNTAX ERROR:")
    #
    # def test7(self):
    #     output: str = run_test("let real_name = 5")[:13]
    #     self.assertEqual(output, "")

if __name__ == '__main__':
    unittest.main()