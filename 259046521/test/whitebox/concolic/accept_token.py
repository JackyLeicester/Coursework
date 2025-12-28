import string
from fuzzingbook.ConcolicFuzzer import ConcolicTracer, ConcolicGrammarFuzzer, ExpectError, GrammarFuzzer
from src.parser import Parser, IncorrectSyntax
from src.lexer import Lexer
from src.evaluator import evaluate
from src.tokens import Token
from fuzzingbook.Grammars import extend_grammar, is_valid_grammar

LANGUAGE_GRAMMAR = extend_grammar({
    "<start>": ["<statement>"],
    "<statement>" : ["<initialisation>"],
    "<initialisation>" : ["let <identifier> = <expression>;"],
    "<identifier>" : list(string.ascii_letters),
    "<expression>" : list(string.digits)
})

assert is_valid_grammar(LANGUAGE_GRAMMAR)

def testing_method(text: str):
    lexer = Lexer(text)
    parser = Parser(lexer)
    statements = parser.run()
    evaluate(statements)

# with ConcolicTracer() as tracer:
#     tracer[testing_method]("let a = 2;")
# scf = ConcolicGrammarFuzzer(LANGUAGE_GRAMMAR)
# for i in range(20):
#     v = scf.fuzz()
#     if v is None:
#         break
#     print(repr(v))
#     with ExpectError(print_traceback=False):
#         with ConcolicTracer() as tracer:
#             tracer[testing_method](v)
    # scf.add_trace(tracer, v)

gf = GrammarFuzzer(LANGUAGE_GRAMMAR)
for _ in range(10):
    query = gf.fuzz()
    print(repr(query))
    try:
        res = testing_method(query)
        print(repr(res))
    except IncorrectSyntax as e:
        print("> ", e)
        pass
    except:
        break
    print()