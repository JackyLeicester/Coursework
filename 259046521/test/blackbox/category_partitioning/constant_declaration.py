from src.lexer import Lexer
from src.parser import Parser
import unittest


def run_test(test_input: str) -> str:
    # buffer: StringIO = capture_output()
    lexer: Lexer = Lexer(test_input)
    parser: Parser = Parser(lexer)
    parser.run()
    return ""


def expect_exception(tester: unittest.TestCase, test_input: str):
    with tester.assertRaises(Exception):
        lexer: Lexer = Lexer(test_input)
        parser: Parser = Parser(lexer)
        parser.run()


class ConstantDeclarationTest(unittest.TestCase):
    def test1(self):
        expect_exception(self, "const true")

    def test2(self):
        expect_exception(self, "const false")

    def test3(self):
        expect_exception(self, "const true")

    def test4(self):
        expect_exception(self, "const real_name ?")

    def test5(self):
        expect_exception(self, "const real_name ==")

    def test6(self):
        expect_exception(self, "const real_name HAM")

    def test7(self):
        output: str = run_test("const realname = 5")
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
