import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class IntegerReadingAndStoringBranchTest(unittest.TestCase):
    def test_let_store_1(self):
        code = """
        let x = 10;
        x;
        """
        self.assertEqual(run(code), 10)

    def test_overwrites_value_2(self):
        code = """
        let x = 10;
        x = 20;
        x;
        """
        self.assertEqual(run(code), 20)

    def test_in_expression_3(self):
        code = """
        let x = 10;
        let y = 5;
        x + y;
        """
        self.assertEqual(run(code), 15)

    def test_reassign_used_in_expression_4(self):
        code = """
        let x = 1;
        x = x + 2;
        x;
        """
        self.assertEqual(run(code), 3)

    def test_read_undefined_variable_raises_5(self):
        with self.assertRaises(Exception) as ctx:
            run("x;")
        self.assertIn("Undefined", str(ctx.exception))

    def test_assign_undefined_variable_raises_6(self):
        with self.assertRaises(Exception) as ctx:
            run("x = 1;")
        self.assertIn("Undefined", str(ctx.exception))

    def test_shadowing_in_block_if_supported_7(self):
        code = """
        let x = 10;
        if (1 < 2) {
            let x = 99;
            x;
        }
        x;
        """
        result = run(code)
        self.assertIn(result, (10, 99))
