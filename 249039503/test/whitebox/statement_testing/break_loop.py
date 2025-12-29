import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestBreakLoopStatement(unittest.TestCase):
    def test_for_zero_iterations(self):
        program = """
        for(let i = 0; i < 0; i = i + 1) {
            break;
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 0)

    def test_break_exits_loop(self):
        program = """
        for(let i = 0; i < 5; i = i + 1) {
            break;
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 0)

    def test_break_outside_loop_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("break;")
        self.assertIn("break used outside loop", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
