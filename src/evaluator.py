import math
from typing import Any, Dict
from .parser import (
    Expression,
    IntegerLiteral,
    FloatLiteral,
    BooleanLiteral,
    PrefixExpression,
    InfixExpression,
    Identifier,
    LetStatement,
    ConstStatement,
    AssignExpression,
    BlockStatement,
    IfExpression,
    ExpressionStatement,
    CallExpression,
)
from .tokens import Token


class RuntimeEvaluationError(Exception):
    pass


Env = Dict[str, tuple[Any, bool]]


def _get_var(env: Env, name: str) -> Any:
    if name not in env:
        raise RuntimeEvaluationError(f"Undefined variable '{name}'")
    return env[name][0]


def _declare_var(env: Env, name: str, value: Any, is_const: bool) -> Any:
    if name in env and env[name][1]:
        raise RuntimeEvaluationError(f"Cannot redeclare constant '{name}'")
    env[name] = (value, is_const)
    return value


def _assign_var(env: Env, name: str, value: Any) -> Any:
    if name not in env:
        raise RuntimeEvaluationError(f"Undefined variable '{name}'")
    old_value, is_const = env[name]
    if is_const:
        raise RuntimeEvaluationError(f"Cannot assign to constant '{name}'")
    env[name] = (value, False)
    return value


def _eval(node: Expression, env: Env) -> Any:
    if isinstance(node, IntegerLiteral):
        return int(node.value)

    if isinstance(node, FloatLiteral):
        return float(node.value)

    if isinstance(node, BooleanLiteral):
        return bool(node.literal)

    if isinstance(node, Identifier):
        return _get_var(env, node.name)

    if isinstance(node, CallExpression):
        name = node.identifier_name
        args = [_eval(arg, env) for arg in node.parameters]
        if name == "sqrt":
            if len(args) != 1:
                raise RuntimeEvaluationError("sqrt expects 1 arguments")
            return float(math.sqrt(args[0]))
        if name == "pow":
            if len(args) != 2:
                raise RuntimeEvaluationError("pow expects 2 arguments")
            return float(math.pow(args[0], args[1]))
        if name == "ceil":
            if len(args) != 1:
                raise RuntimeEvaluationError("ceil expects 1 arguments")
            return int(math.ceil(args[0]))
        if name == "floor":
            if len(args) != 1:
                raise RuntimeEvaluationError("floor expects 1 arguments")
            return int(math.floor(args[0]))
        if name == "abs":
            if len(args) != 1:
                raise RuntimeEvaluationError("abs expects 1 arguments")
            return abs(args[0])

        raise RuntimeEvaluationError(f"Unsupported function '{name}'")

    if isinstance(node, PrefixExpression):
        right = _eval(node.right, env) if node.right is not None else None
        op = node.token
        if op == Token.MINUS:
            return -right
        if op == Token.PLUS:
            return +right
        if op == Token.NOT:
            return not bool(right)
        raise RuntimeEvaluationError(f"Unsupported prefix operator '{op}'")

    if isinstance(node, InfixExpression):
        left = _eval(node.lhs, env)
        right = _eval(node.rhs, env)
        t = node.operation

        # arithmetic
        if t == Token.PLUS:
            return left + right
        if t == Token.MINUS:
            return left - right
        if t == Token.ASTERISK:
            return left * right
        if t == Token.SLASH:
            if right == 0:
                raise RuntimeEvaluationError("Division by zero")
            return left / right

        # comparisons
        if t == Token.EQUAL:
            return left == right
        if t == Token.NOTEQUAL:
            return left != right
        if t == Token.LESS:
            return left < right
        if t == Token.LESSEQUAL:
            return left <= right
        if t == Token.GREATER:
            return left > right
        if t == Token.GREATEREQUAL:
            return left >= right

        # logical
        if t == Token.AND:
            return bool(left) and bool(right)
        if t == Token.OR:
            return bool(left) or bool(right)

        raise RuntimeEvaluationError(f"Unsupported infix operator '{t}'")

    if isinstance(node, LetStatement):
        value = _eval(node.expression, env)
        return _declare_var(env, node.identifier.name, value, is_const=False)

    if isinstance(node, ConstStatement):
        value = _eval(node.expression, env)
        return _declare_var(env, node.identifier.name, value, is_const=True)

    if isinstance(node, AssignExpression):
        if not isinstance(node.lhs, Identifier):
            raise RuntimeEvaluationError(
                "Left-hand side of assignment must be a variable"
            )
        value = _eval(node.rhs, env)
        return _assign_var(env, node.lhs.name, value)

    if isinstance(node, ExpressionStatement):
        if node.expression is None:
            return None
        return _eval(node.expression, env)

    if isinstance(node, BlockStatement):
        result = None
        for stmt in node.statements:
            result = _eval(stmt, env)
        return result

    if isinstance(node, IfExpression):
        cond = _eval(node.condition, env)
        if cond:
            return _eval(node.consequence, env) if node.consequence else None
        return _eval(node.alternative, env) if node.alternative else None

    raise RuntimeEvaluationError(
        f"Evaluation not implemented for node type {type(node).__name__}"
    )


def evaluate(expressions: list[Expression], env: Env | None = None) -> Any:
    if env is None:
        env = {}
    result = None
    for expression in expressions:
        result = _eval(expression, env)
    return result
