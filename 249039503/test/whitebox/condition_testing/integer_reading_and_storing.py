import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestIntegerReadAndStoreCondition(unittest.TestCase):
    def test_isInt_numeric_string_true_1(self):
        self.assertEqual(evaluate_expr('isInt("123");'), True)

    def test_isInt_non_numeric_string_false_2(self):
        self.assertEqual(evaluate_expr('isInt("12a");'), False)

    def test_toInt_from_float_truncates_like_python_3(self):
        self.assertEqual(evaluate_expr("toInt(3.9);"), 3)

    def test_toInt_wrong_arity_raises_4(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("toInt();")
        self.assertIn("to_int expects 1 argument", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
