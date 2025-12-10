import unittest
from src.evaluator import evaluate_expr


class NestingMathOperationsTest(unittest.TestCase):
    def _eval(self, expr: str):
        return evaluate_expr(expr)

    def test1(self):
        self.assertEqual(self._eval("1 + 2 + 3"), 6)

    def test2(self):
        self.assertEqual(self._eval("1 * (2 + 3)"), 5)

    def test3(self):
        self.assertEqual(self._eval("1 * (2 * (3 + 4))"), 14)

    def test4(self):
        self.assertEqual(self._eval("(-1 + (2 + (3 - (4 - 5))))"), 5)

    def test5(self):
        self.assertEqual(self._eval("(1 + 2) - (3 + 4)"), -4)

    def test6(self):
        self.assertEqual(self._eval("(8/2)*(4*2)"), 32)

    def test7(self):
        self.assertEqual(self._eval("(1+2) * (3-2) + 4/2"), 5)

    def test8(self):
        self.assertEqual(self._eval("(1+(2*3))"), 7)

    def test9(self):
        self.assertEqual(self._eval("0 + (1 + (2 + 0))"), 3)

    def test10(self):
        self.assertEqual(self._eval("(-1) + (2*3)"), 5)

    def test11(self):
        self.assertEqual(self._eval("(-1) + (2 * (-3))"), -7)

    def test12(self):
        self.assertEqual(self._eval("1+(2*(3+4))"), 15)

    def test13(self):
        self.assertEqual(self._eval(" 1+ ( 2*  (3+4 ) ) "), 15)

    def test14(self):
        with self.assertRaises(Exception):
            self._eval("1+(2*(3+4)")  # bracket missing


if __name__ == "__main__":
    unittest.main()
