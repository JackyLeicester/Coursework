import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import _eval, RuntimeEvaluationError


class TestArithmeticOperationsCondition(unittest.TestCase):
    def _run(self, code: str):
        lexer = Lexer(code)
        parser = Parser(lexer)
        expressions = parser.run()
        env = {}
        result = None
        for e in expressions:
            if e is None:
                continue
            result = _eval(e, env)
        return result

    # -------- Division condition: right == 0 vs right != 0 --------
    def test_division_right_nonzero_int(self):
        self.assertEqual(self._run("10/2"), 5)

    def test_division_right_nonzero_float(self):
        self.assertAlmostEqual(self._run("7.5/2.5"), 3.0, places=6)

    def test_division_right_zero_int_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            self._run("10/0")
        self.assertIn("Division by zero", str(ctx.exception))

    def test_division_right_zero_float_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            self._run("10.0/0.0")
        self.assertIn("Division by zero", str(ctx.exception))

    # -------- Operator selection: + - * --------
    def test_plus_int_int(self):
        self.assertEqual(self._run("1+2"), 3)

    def test_minus_int_int(self):
        self.assertEqual(self._run("5-8"), -3)

    def test_multiply_int_int(self):
        self.assertEqual(self._run("3*4"), 12)

    def test_plus_int_float(self):
        self.assertAlmostEqual(self._run("1+2.5"), 3.5, places=6)

    def test_multiply_float_int(self):
        self.assertAlmostEqual(self._run("2.5*2"), 5.0, places=6)

    # -------- Bitwise condition: integer operands required --------
    # Decision:
    # if t == BITWISE_AND/OR/XOR:
    #   _check_integer_operands(left, right) -> raises if not both int

    def test_bitwise_and_requires_integers_left_float_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            self._run("1.5 & 1")
        self.assertIn("Bitwise operations require integers", str(ctx.exception))

    def test_bitwise_or_requires_integers_right_float_raises(self):
        with self.assertRaises(RuntimeEvaluationError) as ctx:
            self._run("1 | 2.0")
        self.assertIn("Bitwise operations require integers", str(ctx.exception))

    def test_bitwise_xor_ok_ints(self):
        self.assertEqual(self._run("5 ^ 3"), 6)  # 0101 ^ 0011 = 0110

    # -------- Logical condition (still within InfixExpression) --------
    # Decision:
    # if t == AND: return bool(left) and bool(right)
    # if t == OR:  return bool(left) or bool(right)
    def test_logical_and_truth_table_case(self):
        self.assertEqual(self._run("true && false"), False)

    def test_logical_or_truth_table_case(self):
        self.assertEqual(self._run("false || 1"), True)  # bool(1)=True


if __name__ == "__main__":
    unittest.main()
