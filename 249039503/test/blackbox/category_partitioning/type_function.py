import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    parser = Parser(Lexer(program))
    expressions = parser.run()
    return evaluate(expressions)


class TypeFunctionCategoryPartitioningTests(unittest.TestCase):
    def test_type_int_literal_1(self):
        program = """
        type(10);
        """
        self.assertEqual(evaluate_expr(program), "integer")

    def test_type_float_literal_2(self):
        program = """
        type(3.14);
        """
        self.assertEqual(evaluate_expr(program), "float")

    def test_type_bool_literal_3(self):
        program = """
        type(true);
        """
        self.assertEqual(evaluate_expr(program), "boolean")

    def test_type_string_literal_4(self):
        program = """
        type("hello");
        """
        self.assertEqual(evaluate_expr(program), "string")

    def test_type_declared_variable_5(self):
        program = """
        let x = 10;
        type(x);
        """
        self.assertEqual(evaluate_expr(program), "integer")

    def test_type_declared_constant_6(self):
        program = """
        const y = 3.5;
        type(y);
        """
        self.assertEqual(evaluate_expr(program), "float")

    def test_type_expression_result_7(self):
        program = """
        type(1 + 2);
        """
        self.assertEqual(evaluate_expr(program), "integer")

    def test_type_inside_if_8(self):
        program = """
        if (true) {
            type(10);
        }
        """
        self.assertEqual(evaluate_expr(program), "integer")

    def test_type_inside_loop_9(self):
        program = """
        let i = 0;
        while (i < 1) {
            i = i + 1;
            type(i);
        }
        """
        self.assertEqual(evaluate_expr(program), "integer")

    def test_type_no_arguments_10(self):
        program = """
        type();
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_type_multiple_arguments_11(self):
        program = """
        type(1, 2);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_type_undefined_variable_12(self):
        program = """
        type(x);
        """
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_type_function_identifier_13(self):
        program = """
        fn f() {
            return 1;
        };
        type(f);
        """
        self.assertEqual(evaluate_expr(program), "function")
