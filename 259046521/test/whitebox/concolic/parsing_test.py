import string
import unittest
from fuzzingbook.ConcolicFuzzer import (
    ConcolicTracer,
    ConcolicGrammarFuzzer,
    ExpectError,
    GrammarFuzzer,
)
from src.parser import Parser
from src.lexer import Lexer
from fuzzingbook.Grammars import extend_grammar

# concolic testing was done by creating a grammar that the concolic fuzzer could follow
# afterwards the fuzzer generates valid sequences of tokens that follow the grammar set out by the grammar
# this creates a more complete grammar as it will not try to read varaibles that dont exist and therefore the grammar is mroe feature complet
LANGUAGE_GRAMMAR = extend_grammar(
    {
        "<start>": ["<statement>"],
        "<statement>": ["<callable>", "<initialisation>", "<function>", "<return>"],
        "<initialisation>": [
            "let <identifier> = <expression>;",
            "const <identifier> = <expression>;",
        ],
        "<callable>": ["ifExists(<identifier>);", "<identifier>(<parameter>);"],
        "<parameter>": ["", "<identifier>"],
        "<identifier>": list(string.ascii_letters),
        "<expression>": list(string.digits),
        "<function>": ["fn <identifier>(<parameter>){<statement>};"],
        "<return>": ["return <parameter>;"],
    }
)


def thing(input: str):
    input = str(input)
    lexer = Lexer(input)
    parser = Parser(lexer)
    parser.run()


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
