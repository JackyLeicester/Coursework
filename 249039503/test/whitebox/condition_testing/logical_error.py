import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError


def evaluate_expr(program: str):
    expressions = Parser(Lexer(program)).run()
    return evaluate(expressions)


class TestLogicalErrorCondition(unittest.TestCase):
    def test_undefined_variable_read_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("x;")
        self.assertIn("Undefined variable 'x'", str(ctx.exception))

    def test_undefined_variable_assignment_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("x = 1;")
        self.assertIn("Undefined variable 'x'", str(ctx.exception))

    def test_redeclare_constant_in_same_scope_raises(self):
        program = """
        const x = 1;
        const x = 2;
        """
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("Cannot redeclare constant 'x'", str(ctx.exception))

    def test_assign_to_constant_raises(self):
        program = """
        const x = 1;
        x = 2;
        """
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("Cannot assign to constant 'x'", str(ctx.exception))

    def test_assignment_lhs_not_identifier_raises(self):
        program = "(1 + 2) = 3;"
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr(program)
        self.assertIn("Left-hand side of assignment must be a variable", str(ctx.exception))

    def test_break_outside_loop_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("break;")
        self.assertIn("break used outside loop", str(ctx.exception))

    def test_continue_outside_loop_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            evaluate_expr("continue;")
        self.assertIn("continue used outside loop", str(ctx.exception))

    def test_let_variable_ok_then_assign_ok(self):
        program = """
        let x = 1;
        x = 2;
        x;
        """
        self.assertEqual(evaluate_expr(program), 2)

    def test_shadowing_constant_in_inner_scope_is_allowed(self):
        program = """
        let x = 1;
        let x = 2;
        x;
        """
        self.assertEqual(evaluate_expr(program), 2)


if __name__ == "__main__":
    unittest.main()
