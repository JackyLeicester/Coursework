import unittest

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate


def evaluate_expr(program: str):
    parser = Parser(Lexer(program))
    expressions = parser.run()
    return evaluate(expressions)


class BreakStatementCategoryPartitioningTests(unittest.TestCase):
    def test_break_1(self):
        program = """
        let i = 0;

        for(let i = 0; i < 5; i = i + 1) {
            i = i;
        }

        i;
        """
        self.assertEqual(evaluate_expr(program), 5)

    def test_break_first_iteration_2(self):
        program = """
        let i = 0;

        for(let i = 0; i < 5; i = i + 1) {
            break;
        }

        i;
        """
        self.assertEqual(evaluate_expr(program), 0)

    def test_break_middle_iteration_3(self):
        program = """
        let i = 0;

        for(let i = 0; i < 10; i = i + 1) {
            if (i == 3) {
                break;
            }
        }

        i;
        """
        self.assertEqual(evaluate_expr(program), 3)

    def test_break_last_iteration_4(self):
        program = """
        let i = 0;

        for(let i = 0; i < 5; i = i + 1) {
            if (i == 4) {
                break;
            }
        }

        i;
        """
        self.assertEqual(evaluate_expr(program), 4)

    def test_break_inner_loop_5(self):
        program = """
        let i = 0;

        for(let i = 0; i < 3; i = i + 1) {
            let j = 0;
            for(let j = 0; j < 5; j = j + 1) {
                if (j == 2) {
                    break;
                }
            }
        }

        i;
        """
        self.assertEqual(evaluate_expr(program), 3)

    def test_break_outside_loop_6(self):
        program = "break;"
        with self.assertRaises(Exception):
            evaluate_expr(program)

    def test_assignment_works_7(self):
        program = """
        let x = 1;
        x = x + 1;
        x;
        """
        self.assertEqual(evaluate_expr(program), 2)


if __name__ == "__main__":
    unittest.main()
