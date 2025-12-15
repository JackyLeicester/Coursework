from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import _eval, Env, _get_var
import unittest

class VariableShadowingTester(unittest.TestCase):
    def test1(self):
        test_string: str = """
        let a = 3;
        fn thing():
            let a = 2;
        """
        lexer: Lexer = Lexer(test_string)
        parser: Parser = Parser(lexer)
        expressions = parser.run()
        env: Env
        # _eval(expressions[0], env)
        # self.assertEqual(_get_var(env, 'a'), 3)
        # _eval(expressions[1], env)
        # _eval(expressions[2], env)
        # self.assertEqual(_get_var(env, 'a'), 2)
        # _eval(expressions[3], env)
        # self.assertEqual(_)

    