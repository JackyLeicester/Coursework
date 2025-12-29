import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestIntegerReadingAndStoringLoopTesting(unittest.TestCase):
    # Case 1: Zero conversions/stores
    def test_zero_conversions_store_direct_int(self):
        program = """
        let x = 5;
        x;
        """
        self.assertEqual(evaluate_expr(program), 5)

    # Case 2: One conversion/store
    def test_one_conversion_and_store(self):
        program = """
        let x = toInt("10");
        x;
        """
        self.assertEqual(evaluate_expr(program), 10)

    # Case 3: Multiple conversions/stores
    def test_multiple_conversions_and_stores(self):
        program = """
        let a = toInt("1");
        let b = toInt("2");
        let c = toInt("3");
        a + b + c;
        """
        self.assertEqual(evaluate_expr(program), 6)


if __name__ == "__main__":
    unittest.main()
