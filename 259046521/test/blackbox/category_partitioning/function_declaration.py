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
        expect_exception(self, "true")

    def test2(self):
        expect_exception(self, "false")

    def test3(self):
        expect_exception(self, "real_name)")

    def test4(self):
        expect_exception(self, "real_name(")

    def test5(self):
        expect_exception(self, "real_name((")

    def test6(self):
        expect_exception(self, "real_name(A")

    def test7(self):
        expect_exception(self, "real_name()}}")

    def test8(self):
        expect_exception(self, "real_name()A")

    def test9(self):
        expect_exception(self, "real_name(){{{{")

    def test10(self):
        expect_exception(self, "real_name(){{)")

    def test11(self):
        expect_exception(self, "real_name(){{}}")

    def test12(self):
        expect_exception(self, "real_name(){{}}AA")

    def test13(self):
        output: str = run_test("real_name(){{}};")
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
