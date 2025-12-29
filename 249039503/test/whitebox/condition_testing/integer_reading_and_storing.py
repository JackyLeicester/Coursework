import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestIntegerReadAndStoreCondition(unittest.TestCase):

    def test_isInt_numeric_string_true(self):
        self.assertEqual(evaluate_expr('isInt("123");'), True)

    def test_isInt_non_numeric_string_false(self):
        self.assertEqual(evaluate_expr('isInt("12a");'), False)

    def test_isInt_empty_string_false(self):
        self.assertEqual(evaluate_expr('isInt("");'), False)

    def test_isInt_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr('isInt("1", "2");')
        self.assertIn("is_int expects 1 argument", str(ctx.exception))

    def test_isInt_non_string_raises(self):
        with self.assertRaises(Exception):
            evaluate_expr("isInt(123);")

    def test_toInt_from_numeric_string_success(self):
        self.assertEqual(evaluate_expr('toInt("42");'), 42)

    def test_toInt_from_int_success(self):
        self.assertEqual(evaluate_expr("toInt(7);"), 7)

    def test_toInt_from_float_truncates_like_python(self):
        self.assertEqual(evaluate_expr("toInt(3.9);"), 3)

    def test_toInt_from_non_numeric_string_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr('toInt("4a");')
        self.assertIn("Cannot convert value to int", str(ctx.exception))

    def test_toInt_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("toInt();")
        self.assertIn("to_int expects 1 argument", str(ctx.exception))

    def test_store_converted_int_in_variable(self):
        program = """
        let x = toInt("10");
        x;
        """
        self.assertEqual(evaluate_expr(program), 10)

    def test_update_variable_with_int_value(self):
        program = """
        let x = toInt("10");
        x = x + 5;
        x;
        """
        self.assertEqual(evaluate_expr(program), 15)


if __name__ == "__main__":
    unittest.main()
