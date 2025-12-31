from z3 import *

from src.parser import ForStatement
from src import Lexer, Parser


def build_for_statement(for_ok, lpar_ok, semi1_ok, semi2_ok, rpar_ok):
    parts = []
    parts.append("for" if for_ok else "fr")
    parts.append(" " )
    parts.append("(" if lpar_ok else " ")
    parts.append("let x = 0" )
    parts.append(";" if semi1_ok else " ")
    parts.append(" x < 10" )
    parts.append(";" if semi2_ok else " ")
    parts.append(" x = x + 1" )
    parts.append(")" if rpar_ok else " ")
    parts.append(" { }")
    return "".join(parts)


def parse_for_statement(src: str):
    lexer = Lexer(src)
    parser = Parser(lexer)
    try:
        res = parser.parse_for_statement()
        return "ok", res
    except Exception:
        return "err", None

def test_for_statement():
    for_ok = Bool("for_ok")
    lpar_ok = Bool("lpar_ok")
    semi1_ok = Bool("semi1_ok")
    semi2_ok = Bool("semi2_ok")
    rpar_ok = Bool("rpar_ok")

    s = Solver()
    s.add(And(for_ok, lpar_ok, semi1_ok, semi2_ok, rpar_ok))
    if s.check() == "sat":
        print(s.model())
        src = build_for_statement(True, True, True, True, True)
        tag, node = parse_for_statement(src)
        assert tag == "ok"
        assert isinstance(node, ForStatement)
