from typing import Any, Dict, List

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
    FunctionStatement
)
from .tokens import Token


class RuntimeEvaluationError(Exception):
    pass


Env = List[Dict[str, tuple[Any, bool]]]
Context = Dict[str, tuple[Any, bool]]


def _get_var(env: Env, name: str) -> Any:
    for context in env[::-1]:
        if name in context:
            return context[0]
    raise RuntimeEvaluationError(f"Undefined variable '{name}'")


def _declare_var(env: Env, name: str, value: Any, is_const: bool) -> Any:
    if name in env[-1] and env[-1][name][1]:
        raise RuntimeEvaluationError(f"Cannot redeclare constant '{name}'")
    env[-1][name] = (value, is_const)
    return value

def _assign_var(env: Env, name: str, value: Any) -> Any:
    context: Context = _get_declaration_context(env, name)
    _, is_const = context[name]
    if is_const:
        raise RuntimeEvaluationError(f"Cannot assign to constant '{name}'")
    env[name] = (value, False)
    return value

def _get_declaration_context(env: Env, name: str) -> Context:
    for context in env[::-1]:
        if name in context:
            return context
    raise RuntimeEvaluationError(f"Undefined variable '{name}'")

def _eval(node: Expression, env: Env) -> Any:
    if isinstance(node, IntegerLiteral):
        return int(node.value)

    if isinstance(node, FloatLiteral):
        return float(node.value)

    if isinstance(node, BooleanLiteral):
        return bool(node.literal)

    if isinstance(node, Identifier):
        return _get_var(env, node.name)

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
        print(f'assigned let value of name: {node.identifier}')
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

    if isinstance(node, CallExpression):
        env.append(dict())
        function = _get_var(env, node.identifier_name)
        if not isinstance(function, FunctionStatement):
            raise RuntimeError(
                "Looked for function but found another identifier instead"
            )
        result = _eval(node.block)
        env.pop()
        return result

    if isinstance(node, FunctionStatement):
        _assign_var(env, node.identifier, node)
        print(f'assinged function with name: {node.identifier}')
        return None

    raise RuntimeEvaluationError(
        f"Evaluation not implemented for node type {type(node).__name__}"
    )

def evaluate(expressions: List[Expression], env: Env = [dict()]) -> Any:
    print(f'expressions length: {len(expressions)}')
    for expression in expressions:
        print("type", expression, type(expression))
    for expression in expressions:
        print(_eval(expression, env))
