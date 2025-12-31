from z3 import *

from src.parser import IfExpression
from src import Lexer, Parser


def build_if_expression(if_ok, cond_ok, cons_ok, else_ok, alt_ok):
    parts = []
    parts.append("if" if if_ok else "i f")
    parts.append(" ")
    parts.append("x < 1" if cond_ok else "x < ")
    parts.append(" ")
    parts.append("{ 42; }" if cons_ok else "{ 42 ")

    if else_ok is None:
        pass
    else:
        parts.append(" ")
        parts.append("else" if else_ok else "els")
        parts.append(" ")
        parts.append("{ 43; }" if alt_ok else "{ 43 ")
    return "".join(parts)

def parse_if(src: str):
    lexer = Lexer(src)
    parser = Parser(lexer)
    try:
        node = parser.parse_if_expression()
        return "ok", node
    except Exception:
        return "err", None

def test_if_expression_all_good_parses():
    # All parts correct -> should produce IfExpression (no else)
    src = build_if_expression(True, True, True, None, None)
    tag, node = parse_if(src)
    assert tag == "ok"
    assert isinstance(node, IfExpression)

def test_if_expression_with_else_parses():
    # All parts correct -> should produce IfExpression with alternative
    src = build_if_expression(True, True, True, True, True)
    tag, node = parse_if(src)
    assert tag == "ok"
    assert isinstance(node, IfExpression)
    assert node.alternative is not None

def test_if_expression_symbolic_failures():
    s = Solver()
    if_ok = Bool("if_ok")
    cond_ok = Bool("cond_ok")
    cons_ok = Bool("cons_ok")
    else_present = Bool("else_present")
    else_ok = Bool("else_ok")
    alt_ok = Bool("alt_ok")

    # Case: all true + no else -> must parse
    s.push()
    s.add(And(if_ok, cond_ok, cons_ok, Not(else_present)))
    if s.check() == sat:
        src = build_if_expression(True, True, True, None, None)
        tag, node = parse_if(src)
        assert tag == "ok"
        assert isinstance(node, IfExpression)
    s.pop()

    # Case: all true + else present and correct -> must parse with alternative
    s.push()
    s.add(And(if_ok, cond_ok, cons_ok, else_present, else_ok, alt_ok))
    if s.check() == sat:
        src = build_if_expression(True, True, True, True, True)
        tag, node = parse_if(src)
        assert tag == "ok"
        assert isinstance(node, IfExpression)
        assert node.alternative is not None
    s.pop()

    # Check single-point failures (each required part broken) without else
    flags = [
        ("if_ok", False, True, True, None, None),
        ("cond_ok", True, False, True, None, None),
        ("cons_ok", True, True, False, None, None),
    ]
    for name, ifv, condv, consv, elsep, altv in flags:
        src = build_if_expression(ifv, condv, consv, elsep, altv)
        tag, _ = parse_if(src)
        assert tag == "err", f"Parser should fail when {name} is incorrect; src={src!r}"

    # Check failures when else branch present but broken
    else_flags = [
        ("else_ok", True, True, True, True, False),  # else token broken
        ("alt_ok", True, True, True, True, False),   # alt block broken (same src pattern covers both)
    ]
    for name, ifv, condv, consv, elsep, altv in else_flags:
        src = build_if_expression(ifv, condv, consv, elsep, altv)
        tag, _ = parse_if(src)
        assert tag == "err", f"Parser should fail when {name} is incorrect; src={src!r}"
