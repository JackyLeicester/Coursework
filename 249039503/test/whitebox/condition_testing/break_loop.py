import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestBreakLoopCondition(unittest.TestCase):
    def test_for_condition_false_for_zero_iterations(self):
        program = """
        for(let i = 0; i < 0; i = i + 1) {
            break;
        }
        i;
        """
        # If loop does 0 iterations, i is still 0 from initialization.
        self.assertEqual(evaluate_expr(program), 0)

    def test_break_exits_loop_without_increment(self):
        program = """
        for(let i = 0; i < 5; i = i + 1) {
            break;
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 0)

    def test_break_not_taken_loop_runs_to_completion(self):
        program = """
        for(let i = 0; i < 5; i = i + 1) {
            i = i;
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 5)

    def test_break_guard_condition_false_then_true(self):
        program = """
        for(let i = 0; i < 10; i = i + 1) {
            if (i == 3) { break; }
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 3)

    def test_break_only_exits_inner_loop_condition(self):
        program = """
        for(let i = 0; i < 3; i = i + 1) {
            for(let j = 0; j < 5; j = j + 1) {
                if (j == 2) { break; }
            }
        }
        i;
        """
        self.assertEqual(evaluate_expr(program), 3)

    def test_break_outside_loop_raises_specific_error(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("break;")
        self.assertIn("break used outside loop", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
