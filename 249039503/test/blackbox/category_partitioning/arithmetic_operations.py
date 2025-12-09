import unittest
from src.parser import evaluate_expr

class ArithmeticOperationsTest(unittest.TestCase):
    def _eval(self, expr:str):
        return evaluate_expr(expr)

    # Tests for +
    def test1(self):
        self.assertEqual(self._eval('1+2'), 3)
    def test2(self):
        self.assertEqual(self._eval('-7+3'), -4)
    def test3(self):
        self.assertEqual(self._eval('5+0'), 5)
    def test4(self):
        self.assertAlmostEqual(self._eval('5.2*3'), 15.6, places=6)

    # Test for -
    def test5(self):
        self.assertEqual(self._eval('10-5'), 5)
    def test6(self):
        self.assertEqual(self._eval('2-5'), -3)
    def test7(self):
        self.assertEqual(self._eval('9-0'), 9)
    def test8(self):
        self.assertEqual(self._eval('9/2'), 4.5)

    # Test for *
    def test9(self):
        self.assertEqual(self._eval('9*9'), 81)
    def test10(self):
        self.assertEqual(self._eval('-9*1'), -9)
    def test11(self):
        self.assertEqual(self._eval('9*0'), 0)
    def test12(self):
        self.assertEqual(self._eval('2*3.5'), 7)

    # Test for /
    def test13(self):
        self.assertEqual(self._eval('9/3'), 3)
    def test14(self):
        self.assertEqual(self._eval('-9/3'), -3)
    def test15(self):
        self.assertEqual(self._eval('10/4'), 2.5)
    def test16(self):
        with self.assertRaises(Exception):
            self._eval('6/0')

    # Combined different situations
    def test17(self):
        self.assertEqual(self._eval("3+4-2"),5)
    def test18(self):
        self.assertEqual(self._eval(" 5 * 2/1"), 10)
