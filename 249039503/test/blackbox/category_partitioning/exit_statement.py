import unittest

from src.evaluator import evaluate
from src.lexer import Lexer
from src.parser import Parser


def evaluate_expr(program: str):
    parser = Parser(Lexer(program))
    expressions = parser.run()
    return evaluate(expressions)


class ExitStatementCategoryPartitioningTests(unittest.TestCase):
    def test_exit_1(self):
        program = """
        exit(7);
        999;
        """
        self.assertEqual(evaluate_expr(program), 7)

    def test_exit_inside_if_2(self):
        program = """
        if true {
            exit(32 + 24);
        }
        999;
        """
        self.assertEqual(evaluate_expr(program), 56)

    def test_exit_inside_loop_3(self):
        program = """
        let i = 0;
        for (let i = 0; i < 10; i = i + 1) {
            exit(7);
        }
        999;
        """
        self.assertEqual(evaluate_expr(program), 7)

    def test_another_value_error_4(self):
        program = """
        exit(12.5);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_bool_value_raises_error_5(self):
        program = """
        exit(true);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_no_argument_raises_error_6(self):
        program = """
        exit();
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_multiple_arguments_raises_error_7(self):
        program = """
        exit(777, 123);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)


if __name__ == "__main__":
    unittest.main()
