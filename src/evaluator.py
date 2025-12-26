import math
import sys
from typing import Any, Dict, List
from .parser import (
    Expression,
    IntegerLiteral,
    FloatLiteral,
    BooleanLiteral,
    CharLiteral,
    StringLiteral,
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
    ForStatement,
    ContinueStatement,
    BreakStatement,
    FunctionStatement,
    ReturnStatement,
)
from .tokens import Token


class _BreakSignal(Exception):
    pass


class _ContinueSignal(Exception):
    pass


class _ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class RuntimeEvaluationError(Exception):
    pass


Env = List[Dict[str, tuple[Any, bool]]]
Context = Dict[str, tuple[Any, bool]]


def _get_var(env: Env, name: str) -> Any:
    for context in env[::-1]:
        if name in context:
            return context[name][0]
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

    if isinstance(node, CharLiteral):
        return str(node.literal)

    if isinstance(node, StringLiteral):
        return str(node.literal)

    if isinstance(node, Identifier):
        return _get_var(env, node.name)

    if isinstance(node, CallExpression):
        name = node.identifier_name
        args = [_eval(arg, env) for arg in node.parameters]
        if name == "sqrt":
            if len(args) != 1:
                raise RuntimeEvaluationError("sqrt expects 1 arguments")
            return float(math.sqrt(args[0]))
        elif name == "pow":
            if len(args) != 2:
                raise RuntimeEvaluationError("pow expects 2 arguments")
            return float(math.pow(args[0], args[1]))
        elif name == "ceil":
            if len(args) != 1:
                raise RuntimeEvaluationError("ceil expects 1 arguments")
            return int(math.ceil(args[0]))
        elif name == "floor":
            if len(args) != 1:
                raise RuntimeEvaluationError("floor expects 1 arguments")
            return int(math.floor(args[0]))
        elif name == "abs":
            if len(args) != 1:
                raise RuntimeEvaluationError("abs expects 1 arguments")
            return abs(args[0])
        elif name == "println":
            print(*args)
            return None
        elif name == "print":
            print(*args, end="")
            return None
        elif name == "input":
            if len(args) > 0:
                raise RuntimeEvaluationError("abs expects 0 or 1 arguments")
            elif len(args) == 0:
                return input()
            else:
                return input(args[0])
        else:
            env.append(dict())
            function = _get_var(env, node.identifier_name)[0]
            if not isinstance(function, FunctionStatement):
                raise RuntimeError(
                    "Looked for function but found another identifier instead"
                )
            if len(node.parameters) != len(function.variables):
                raise RuntimeError(
                    "Number of parameters passed is not equal to number of function parameters"
                )
            for identifier, expression in zip(function.variables, node.parameters):
                _declare_var(env, identifier.name, _eval(expression, env), False)
            try:
                result = _eval(function.block, env)
                env.pop()
                return result
            except _ReturnSignal:
                _, value, _ = sys.exc_info()
                env.pop()
                return value.value

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

    if isinstance(node, ContinueStatement):
        raise _ContinueSignal()
    if isinstance(node, BreakStatement):
        raise _BreakSignal()

    if isinstance(node, ForStatement):
        _eval(node.initialization, env)

        result = None
        while bool(_eval(node.condition, env)):
            try:
                result = _eval(node.block, env)
            except _ContinueSignal:
                _eval(node.increment, env)
                continue
            except _BreakSignal:
                break

            _eval(node.increment, env)

        return result
    if isinstance(node, FunctionStatement):
        _declare_var(env, node.identifier.name, node, True)
        return None

    if isinstance(node, ReturnStatement):
        evaluation = _eval(node.expression, env)
        if evaluation is tuple:
            raise _ReturnSignal(evaluation[0])
        else:
            raise _ReturnSignal(evaluation)

    raise RuntimeEvaluationError(
        f"Evaluation not implemented for node type {type(node).__name__}"
    )


def evaluate(expressions: list[Expression], env: Env | None = None) -> Any:
    if env is None:
        env = [{}]
    result = None
    try:
        for expression in expressions:
            result = _eval(expression, env)
    except _ReturnSignal:
        _, value, _ = sys.exc_info()
        return "User error code: " + str(value)
    except _ContinueSignal:
        raise RuntimeEvaluationError("continue used outside loop")
    except _BreakSignal:
        raise RuntimeEvaluationError("break used outside loop")
    return result
