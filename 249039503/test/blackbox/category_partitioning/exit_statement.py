import unittest

from src.evaluator import evaluate
from src.lexer import Lexer
from src.parser import Parser


def evaluate_expr(program: str):
    parser = Parser(Lexer(program))
    expressions = parser.run()
    return evaluate(expressions)


class ExitStatementCategoryPartitioningTests(unittest.TestCase):

    def test_top_level_int_literal_immediate_termination(self):
        program = """
        exit(7);
        999;
        """
        self.assertEqual(evaluate_expr(program), 7)

    def test_inside_if_int_expression_immediate_termination(self):
        program = """
        if true {
            exit(3 + 4);
        }
        999;
        """
        self.assertEqual(evaluate_expr(program), 7)

    def test_inside_loop_int_literal_immediate_termination(self):
        program = """
        let i = 0;
        for (i = 0; i < 10; i = i + 1) {
            exit(7);
        }
        999;
        """
        self.assertEqual(evaluate_expr(program), 7)

    # -----------------------
    # INVALID: ERROR RAISED
    # -----------------------

    def test_non_int_value_raises_error(self):
        program = """
        exit(1.5);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_bool_value_raises_error(self):
        program = """
        exit(true);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_no_argument_raises_error(self):
        program = """
        exit();
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_multiple_arguments_raises_error(self):
        program = """
        exit(1, 2);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)


if __name__ == "__main__":
    unittest.main()
