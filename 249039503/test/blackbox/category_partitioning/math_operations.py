import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import _eval


class MathOperationsTest(unittest.TestCase):
    def _eval(self, expr: str):
        lexer = Lexer(expr)
        parser = Parser(lexer)
        expressions = parser.run()
        env = {}
        result = None
        for e in expressions:
            result = _eval(e, env)
        return result

    def test1(self):
        self.assertEqual(self._eval("1 + 2 + 3"), 6)

    def test2(self):
        self.assertEqual(self._eval("1 * 2 + 3"), 5)

    def test3(self):
        self.assertEqual(self._eval("1 * 2 * 3 + 4"), 10)

    def test4(self):
        self.assertEqual(self._eval("-1 + 2 + 3 - 4 - 5"), -5)

    def test5(self):
        self.assertEqual(self._eval("1 + 2 - 3 + 4"), 4)

    def test6(self):
        self.assertEqual(self._eval("8 / 2 * 4 + 2"), 18)

    def test7(self):
        self.assertEqual(self._eval("1 + 2 * 3 - 2 + 4 / 2"), 7)

    def test8(self):
        self.assertEqual(self._eval("1 + 2 * 3"), 7)

    def test9(self):
        self.assertEqual(self._eval("0 * 1 + 2 * 0"), 0)

    def test10(self):
        self.assertEqual(self._eval("-1 + 2 * 3"), 5)

    def test11(self):
        self.assertEqual(self._eval("(-1) + 2 * (-3)"), -7)

    def test12(self):
        self.assertEqual(self._eval("1 + 2 * 3 + 4"), 11)

    def test13(self):
        self.assertEqual(self._eval("1 + 2 * 3 + 4"), 11)


if __name__ == "__main__":
    unittest.main()
