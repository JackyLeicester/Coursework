import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate

# Here I did concolic testing for type() function.  Combine some statements to showing how program works.
# For input comes f.e. type(10) which do path (Lexer -> Parser -> Evaluator)
# In every Run we use concrete argument and save it.
# In this function we can see this path:
# Checking amount of arguments
# If argument is identifier, program checks is it created in environment
# identifier defined
# identifier undefined
# Identifying type of var.


def eval_program(program: str):
    parser = Parser(Lexer(program))
    stmts = parser.run()
    return evaluate(stmts)


class ConcolicTypeFunctionTests(unittest.TestCase):
    def test_T0_seed_int(self):
        self.assertEqual(eval_program("type(10);"), "integer")

    def test_T1_negate_arity_zero_args(self):
        with self.assertRaises(Exception):
            eval_program("type();")

    def test_T2_negate_arity_many_args(self):
        with self.assertRaises(Exception):
            eval_program("type(1, 2);")

    def test_T3_negate_value_type_float(self):
        self.assertEqual(eval_program("type(3.14);"), "float")

    def test_T4_negate_value_type_bool(self):
        self.assertEqual(eval_program("type(true);"), "boolean")

    def test_T5_negate_value_type_string(self):
        self.assertEqual(eval_program('type("hello");'), "string")

    def test_T6_negate_identifier_defined(self):
        with self.assertRaises(Exception):
            eval_program("type(x);")

    def test_T7_identifier_defined_via_let(self):
        self.assertEqual(eval_program("let x = 10; type(x);"), "integer")

    def test_T8_function_identifier(self):
        self.assertEqual(eval_program("fn f(){ return 1; }; type(f);"), "function")


if __name__ == "__main__":
    unittest.main()
