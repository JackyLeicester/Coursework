import string
import unittest
from fuzzingbook.ConcolicFuzzer import (
    ConcolicTracer,
    ConcolicGrammarFuzzer,
    ExpectError,
)
from src.parser import Parser
from src.lexer import Lexer
from src.evaluator import evaluate
from fuzzingbook.Grammars import extend_grammar

LANGUAGE_GRAMMAR = extend_grammar(
    {
        "<start>": ["<statement>"],
        "<statement>": ["<initialisation>", "<function>", "<return>"],
        "<initialisation>": [
            "let <identifier> = <expression>;",
            "const <identifier> = <expression>;",
        ],
        "<parameter>": ["", "<identifier>"],
        "<identifier>": list(string.ascii_letters),
        "<expression>": list(string.digits),
        "<function>": ["fn <identifier>(<parameter>){<statement>};"],
        "<return>": ["return ;"],
    }
)


def thing(input: str):
    input = str(input)
    lexer = Lexer(input)
    parser = Parser(lexer)
    statements = parser.run()
    evaluate(statements)


class ParseTest(unittest.TestCase):
    def test_parsing(self):
        with ConcolicTracer() as tracer:
            tracer[thing]("let a = 2;")
        scf = ConcolicGrammarFuzzer(LANGUAGE_GRAMMAR)
        scf.prune_tokens([])
        for i in range(20):
            with self.subTest(i=i):
                v = scf.fuzz()
                if v is None:
                    break
                print(repr(v))
                with ExpectError(print_traceback=True):
                    with ConcolicTracer() as tracer:
                        tracer[thing](v)
