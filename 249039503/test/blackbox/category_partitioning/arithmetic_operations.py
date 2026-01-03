import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import _eval
from src.evaluator import RuntimeEvaluationError


class ArithmeticOperationsTest(unittest.TestCase):
    def _eval(self, expr: str):
        lexer = Lexer(expr)
        parser = Parser(lexer)
        expressions = parser.run()
        env = {}
        result = None
        for e in expressions:
            if e is None:
                continue
            result = _eval(e, env)
        return result

    # Tests for +
    def test_for_plus_1(self):
        self.assertEqual(self._eval("999+2"), 1001)

    def test_for_plus_2(self):
        self.assertEqual(self._eval("-300+3"), -297)

    def test_for_plus_3(self):
        self.assertEqual(self._eval("554+0"), 554)

    def test_for_plus_4(self):
        self.assertAlmostEqual(self._eval("5.2*3.0"), 15.6, places=6)

    # Test for -
    def test_for_minus_5(self):
        self.assertEqual(self._eval("225-5"), 220)

    def test_for_minus_6(self):
        self.assertEqual(self._eval("2-500"), -498)

    def test_for_minus_7(self):
        self.assertEqual(self._eval("9123-0"), 9123)

    def test_for_minus_8(self):
        self.assertAlmostEqual(self._eval("9.0/2.0"), 4.5, places=6)

    # Test for *
    def test_for_multiplication_9(self):
        self.assertEqual(self._eval("90*90"), 8100)

    def test_for_multiplcitaion_10(self):
        self.assertEqual(self._eval("-901*1"), -901)

    def test_for_multiplcitaion_11(self):
        self.assertEqual(self._eval("9123*0"), 0)

    def test_for_multiplication_12(self):
        self.assertAlmostEqual(self._eval("2.0*3.5"), 7.0, places=6)

    # Test for /
    def test_for_division_13(self):
        self.assertEqual(self._eval("999/3"), 333)

    def test_for_division_14(self):
        self.assertEqual(self._eval("-903/3"), -301)

    def test_for_division_15(self):
        self.assertAlmostEqual(self._eval("10.0/4.0"), 2.5, places=6)

    def test_for_division_16(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self._eval("6/0")
        self.assertIn("Division by zero", str(context.exception))


if __name__ == "__main__":
    unittest.main()
