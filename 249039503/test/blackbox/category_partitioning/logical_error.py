import unittest
from src.evaluator import _eval, RuntimeEvaluationError
from src.lexer import Lexer
from src.parser import Parser


class LogicalErrorTest(unittest.TestCase):
    def evaluate_expr(self, expr: str):
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

    def test1(self):
        self.assertEqual(self.evaluate_expr("10/2"), 5)

    def test2(self):
        self.assertEqual(self.evaluate_expr("10/2.0"), 5.0)

    def test3(self):
        self.assertEqual(self.evaluate_expr("10/(2+3)"), 2)

    def test4(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("6/0")
        self.assertIn("Division by zero", str(context.exception))

    def test5(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("10/(2-2)")
        self.assertIn("Division by zero", str(context.exception))

    def test6(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("10/0")
        self.assertIn("Division by zero", str(context.exception))

    def test7(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("x + 1")
        self.assertIn("Undefined variable 'x'", str(context.exception))

    def test8(self):
        result = self.evaluate_expr("let x = 1; x + 2;")
        self.assertEqual(result, 3)

    def test9(self):
        result = self.evaluate_expr("const y = 5; y + 1;")
        self.assertEqual(result, 6)

    def test10(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("x = 10;")
        self.assertIn("Undefined variable 'x'", str(context.exception))

    def test11(self):
        result = self.evaluate_expr("let x = 1; x = 2; x;")
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
