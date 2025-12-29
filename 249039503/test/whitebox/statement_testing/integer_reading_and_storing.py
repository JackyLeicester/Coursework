import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestIntegerReadingAndStoringStatement(unittest.TestCase):
    def test_isInt_numeric_string_true(self):
        self.assertEqual(evaluate_expr('isInt("123");'), True)

    def test_isInt_non_numeric_string_false(self):
        self.assertEqual(evaluate_expr('isInt("12a");'), False)

    def test_isInt_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr('isInt("1","2");')
        self.assertIn("is_int expects 1 argument", str(ctx.exception))

    def test_toInt_string_success(self):
        self.assertEqual(evaluate_expr('toInt("42");'), 42)

    def test_toInt_wrong_arity_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr('toInt("1","2");')
        self.assertIn("to_int expects 1 argument", str(ctx.exception))

    def test_toInt_invalid_string_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr('toInt("abc");')
        self.assertIn("Cannot convert value to int", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
