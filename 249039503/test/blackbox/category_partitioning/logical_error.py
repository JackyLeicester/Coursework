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

    def test_no_error_1(self):
        self.assertEqual(self.evaluate_expr("100/2"), 50)

    def test_division_int_to_float_2(self):
        self.assertEqual(self.evaluate_expr("10/2.0"), 5.0)

    def test_nested_operation_3(self):
        self.assertEqual(self.evaluate_expr("10/(2+3)"), 2)

    def test_division_by_zero_4(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("62/0")
        self.assertIn("Division by zero", str(context.exception))

    def test_nested_division_by_zero_5(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("102/(2-2)")
        self.assertIn("Division by zero", str(context.exception))

    def test_division_by_zero_6(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("10/0")
        self.assertIn("Division by zero", str(context.exception))

    def test_undefined_var_7(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("x + 1")
        self.assertIn("Undefined variable 'x'", str(context.exception))

    def test_defined_var_8(self):
        result = self.evaluate_expr("let x = 1123; x + 2;")
        self.assertEqual(result, 1125)

    def test_const_9(self):
        result = self.evaluate_expr("const y = 5345; y + 1;")
        self.assertEqual(result, 5346)

    def test_undefined_var_10(self):
        with self.assertRaises(RuntimeEvaluationError) as context:
            self.evaluate_expr("x = 1000;")
        self.assertIn("Undefined variable 'x'", str(context.exception))

    def test11(self):
        result = self.evaluate_expr("let x = 1; x = 2; x;")
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
