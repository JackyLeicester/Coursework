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
        "<program>": list("<statement>"),
        "<statement>": ["<literal>", "<if_statement>", "<for_stmt>"],
        "<literal>": ["<string>", "<char>"],
        "<char>": ["'<char_inner>'"],
        "<char_inner>": list(string.printable),
        "<string>": ['"<string_inner>"'],
        "<string_inner>": list(string.printable),
        "<if_statement>": ["if <expression> <block> { else <block> }"],
        "<block>": ["{ <block_inner> }"],
        "<block_inner>": list("<statement>"),
        "<expression>": list("<literal>"),
        "<for_stmt>": ["for ( <initialization> ; <condition> ; <update> ) <block>"],
        "<initialization>": ["let x = 1"],  # tested by someone else
        "<condition>": ["<expression>", ""],
        "<update>": ["<expression>", ""],
        "<null>": ["null"],
    }
)


def setup_and_run(src: str):
    lexer = Lexer(str(src))
    parser = Parser(lexer)
    statements = parser.run()
    evaluate(statements)


class TestEvaluator(unittest.TestCase):
    def test_evaluator(self):
        with ConcolicTracer() as tracer:
            tracer[setup_and_run](
                "let a = 2; if a < 2 { print(true); } else { print(false); }"
            )

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
                        tracer[setup_and_run](v)
