import unittest
from src.evaluator import evaluate_expr, RuntimeEvaluationError


class LogicalErrorTest(unittest.TestCase):
    def _eval(self, expr: str):
        return evaluate_expr(expr)

    def test1(self):
        self.assertEqual(self._eval("10/2"), 5)

    def test2(self):
        self.assertEqual(self._eval("10/2.0"), 5.0)

    def test3(self):
        self.assertEqual(self._eval("10/(2+3)"), 2)

    def test4(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self._eval("6/0")
        self.assertIn("Division by zero", str(context.exception))

    def test5(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self._eval("10/(2-2)")
        self.assertIn("Division by zero", str(context.exception))

    def test6(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self._eval("10/0")
        self.assertIn("Division by zero", str(context.exception))

    def test7(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self._eval("x + 1")
        self.assertIn("Undefined variable 'x'", str(context.exception))

    def test8(self):
        result = self._eval("let x = 1; x + 2;")
        self.assertEqual(result, 3)

    def test9(self):
        result = self._eval("const y = 5; y + 1;")
        self.assertEqual(result, 6)

    def test10(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self._eval("x = 10;")
        self.assertIn("Undefined variable 'x'", str(context.exception))

    def test11(self):
        result = self._eval("let x = 1; x = 2; x;")
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
