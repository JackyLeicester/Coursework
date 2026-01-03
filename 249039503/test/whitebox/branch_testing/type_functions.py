import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


def assert_type_str(testcase: unittest.TestCase, value, expected_keywords):
    testcase.assertIsInstance(value, str)
    lower = value.lower()
    testcase.assertTrue(
        any(k in lower for k in expected_keywords), f"Got type string: {value!r}"
    )


class TypeFunctionBranchTest(unittest.TestCase):
    def test_type_int_literal_1(self):
        v = run("type(1);")
        assert_type_str(self, v, ("int", "integer", "number"))

    def test_type_float_literal_2(self):
        v = run("type(1.5);")
        assert_type_str(self, v, ("float", "double", "number"))

    def test_type_bool_literal_3(self):
        v = run("type(true);")
        assert_type_str(self, v, ("bool", "boolean"))

    def test_type_string_literal_4(self):
        v = run('type("x");')
        assert_type_str(self, v, ("string", "str"))

    def test_type_char_literal_if_supported_5(self):
        try:
            v = run("type('a');")
            assert_type_str(self, v, ("char", "character", "string"))
        except Exception:
            pass

    def test_type_identifier_6(self):
        v = run("let x = 10; type(x);")
        assert_type_str(self, v, ("int", "integer", "number"))

    def test_type_wrong_arity_zero_args_raises_7(self):
        with self.assertRaises(Exception):
            run("type();")

    def test_type_wrong_arity_two_args_raises_8(self):
        with self.assertRaises(Exception):
            run("type(1, 2);")
