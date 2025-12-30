import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def run(code: str):
    statements = Parser(Lexer(code)).run()
    return evaluate(statements)


class BreakLoopBranchTest(unittest.TestCase):
    def test_break_exits_loop_immediately(self):
        code = """
        for (let i = 0; i < 10; i = i + 1) {
            break;
            i = i + 100;
        }
        0;
        """
        self.assertEqual(run(code), 0)

    def test_break_after_some_iterations(self):
        code = """
        let out = 0;
        for (let i = 0; i < 10; i = i + 1) {
            out = out + 1;
            if (out == 3) { break; }
        }
        out;
        """
        self.assertEqual(run(code), 3)

    def test_zero_iterations_condition_false_initially(self):
        code = """
        let out = 123;
        for (let i = 0; i < 0; i = i + 1) {
            out = 999;
        }
        out;
        """
        self.assertEqual(run(code), 123)

    def test_break_in_nested_loop_breaks_inner_only(self):
        code = """
        let outer = 0;
        for (let o = 0; o < 2; o = o + 1) {
            for (let i = 0; i < 5; i = i + 1) {
                break;
            }
            outer = outer + 1;
        }
        outer;
        """
        self.assertEqual(run(code), 2)

    def test_break_outside_loop_raises(self):
        with self.assertRaises(Exception):
            run("break;")
