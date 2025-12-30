import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class ExitStatementBranchTest(unittest.TestCase):
    def test_exit_with_code_int_returns_code(self):
        self.assertEqual(run("exit(7);"), 7)

    def test_exit_zero_returns_zero(self):
        self.assertEqual(run("exit(0);"), 0)

    def test_exit_negative_returns_negative(self):
        self.assertEqual(run("exit(-1);"), -1)

    def test_exit_inside_if_returns_code(self):
        code = """
        if (1 < 2) {
            exit(3);
        }
        """
        self.assertEqual(run(code), 3)

    def test_exit_inside_loop_returns_code(self):
        code = """
        for (let i = 0; i < 3; i = i + 1) {
            exit(5);
        }
        """
        self.assertEqual(run(code), 5)

    def test_exit_missing_argument_raises(self):
        with self.assertRaises(Exception):
            run("exit();")

    def test_exit_non_int_argument_raises(self):
        with self.assertRaises(Exception):
            run('exit("1");')
