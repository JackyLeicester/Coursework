import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestTypeFunctionCondition(unittest.TestCase):
    def test_type_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("type();")
        self.assertIn("type expects 1 argument", str(ctx.exception))

    def test_type_two_args_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("type(1, 2);")
        self.assertIn("type expects 1 argument", str(ctx.exception))

    def test_type_null(self):
        self.assertEqual(evaluate_expr("type(null);"), "null")

    def test_type_boolean_true(self):
        self.assertEqual(evaluate_expr("type(true);"), "boolean")

    def test_type_integer(self):
        self.assertEqual(evaluate_expr("type(123);"), "integer")

    def test_type_float(self):
        self.assertEqual(evaluate_expr("type(1.25);"), "float")

    def test_type_string(self):
        self.assertEqual(evaluate_expr('type("abc");'), "string")


if __name__ == "__main__":
    unittest.main()
