from torch._C._jit_tree_views import StringLiteral

from src.lexer import Lexer
from src.parser import (
    Parser,
    IntegerLiteral,
    FloatLiteral,
    PrefixExpression,
    InfixExpression,
)
from src.parser import IntegerLiteral, FloatLiteral, PrefixExpression
from src.tokens import Token


def _eval(node):
    if isinstance(node, (IntegerLiteral, FloatLiteral)):
        text = str(node.value)
        return float(text) if "." in text else int(text)

    if isinstance(node, PrefixExpression):
        right_val = _eval(node.right)
        if node.operator == "+":
            return +right_val
        if node.operator == "-":
            return -right_val
        raise Exception("Unsupported operator: {node.operator}")

    if isinstance(node, InfixExpression):
        left_val = _eval(node.lhs)
        right_val = _eval(node.rhs)

        def _is_int(value):
            return isinstance(value, int) and not isinstance(value, bool)

        def _is_float(value):
            return isinstance(value, float)

        if node.operation in {
            Token.LESS,
            Token.GREATER,
            Token.LESSEQUAL,
            Token.GREATEREQUAL,
        }:
            if not (
                (_is_int(left_val) and _is_int(right_val))
                or (_is_float(left_val) and _is_float(right_val))
            ):
                raise Exception("Infix expression must have same type of operator")

            if node.operation == Token.LESS:
                return left_val < right_val
            if node.operation == Token.GREATER:
                return left_val > right_val
            if node.operation == Token.LESSEQUAL:
                return left_val <= right_val
            if node.operation == Token.GREATEREQUAL:
                return left_val >= right_val

        if node.operation == Token.PLUS:
            return left_val + right_val
        if node.operation == Token.MINUS:
            return left_val - right_val
        if node.operation == Token.ASTERISK:
            return left_val * right_val
        if node.operation == Token.SLASH:
            if right_val == 0:
                raise Exception("Can't divide by zero")
            return left_val / right_val

        raise Exception("Unsupported operator: {node.operation}")


def evaluate_expr(source: str):
    lexer = Lexer(source)
    parser = Parser(lexer)

    expression = parser.parse_expression()
    if expression is None:
        raise Exception("Parse failed")

    return _eval(expression)
