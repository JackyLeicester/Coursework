import math
from typing import Any, Dict, List
from .parser import (
    Expression,
    IntegerLiteral,
    FloatLiteral,
    BooleanLiteral,
    NullLiteral,
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
    WhileStatement,
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


class _ExitSignal(Exception):
    def __init__(self, code: int):  # pragma: no cover
        self.code = code


Env = List[Dict[str, tuple[Any, bool]]]
Context = Dict[str, tuple[Any, bool]]


def _env_stack(env: "Env | Context") -> Env:
    return env if isinstance(env, list) else [env]


def setup_runtime(arg: str) -> Env:
    env: Env = [{}]
    _declare_var(env, "arg", arg, True)
    return env


def _get_var(env: "Env | Context", name: str) -> tuple[Any, bool]:
    stack = _env_stack(env)
    for context in stack[::-1]:
        if name in context:
            return context[name]
    raise RuntimeEvaluationError(f"Undefined variable '{name}'")


def _check_integer_operands(left: Any, right: Any) -> None:
    if not isinstance(left, int) or not isinstance(right, int):
        raise RuntimeEvaluationError("Bitwise operations require integers")


def _declare_var(env: "Env | Context", name: str, value: Any, is_const: bool) -> Any:
    stack = _env_stack(env)
    if name in stack[-1] and stack[-1][name][1]:
        raise RuntimeEvaluationError(f"Cannot redeclare constant '{name}'")
    stack[-1][name] = (value, is_const)
    return value


def _assign_var(env: "Env | Context", name: str, value: Any) -> Any:
    context = _get_declaration_context(env, name)
    _, is_const = context[name]
    if is_const:
        raise RuntimeEvaluationError(f"Cannot assign to constant '{name}'")
    context[name] = (value, False)
    return value


def _get_declaration_context(env: "Env | Context", name: str) -> Context:
    stack = _env_stack(env)
    for context in stack[::-1]:
        if name in context:
            return context
    raise RuntimeEvaluationError(f"Undefined variable '{name}'")


def _is_declared(env: Env, name: str) -> bool:
    try:
        _get_declaration_context(env, name)
        return True
    except RuntimeEvaluationError:
        return False


def _eval(node: Expression, env: "Env | Context") -> Any:
    if isinstance(node, IntegerLiteral):
        return int(node.value)

    if isinstance(node, FloatLiteral):
        return float(node.value)

    if isinstance(node, BooleanLiteral):
        return bool(node.literal)

    if isinstance(node, NullLiteral):
        return None

    if isinstance(node, CharLiteral):
        return str(node.literal)

    if isinstance(node, StringLiteral):
        return str(node.literal)

    if isinstance(node, Identifier):
        val, _is_const = _get_var(env, node.name)
        return val

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
        elif name == "input":  # pragma: no cover
            if len(args) > 1:
                raise RuntimeEvaluationError("input expects 0 or 1 arguments")
            elif len(args) == 0:
                return input()
            return input(str(args[0]))
        elif name == "isInt":
            if len(args) != 1:
                raise RuntimeEvaluationError("is_int expects 1 argument")
            return args[0].isnumeric()
        elif name == "toInt":
            if len(args) != 1:
                raise RuntimeEvaluationError("to_int expects 1 argument")
            try:
                return int(args[0])
            except (ValueError, TypeError):
                raise RuntimeEvaluationError("Cannot convert value to int")
        elif name == "isFloat":
            if len(args) != 1:
                raise RuntimeEvaluationError("is_float expects 1 argument")
            try:
                float(args[0])
                return True
            except (ValueError, TypeError):
                return False
        elif name == "toFloat":
            if len(args) != 1:
                raise RuntimeEvaluationError("to_float expects 1 argument")
            try:
                return float(args[0])
            except (ValueError, TypeError):
                raise RuntimeEvaluationError("Cannot convert value to float")
        elif name == "toStr":
            if len(args) != 1:
                raise RuntimeEvaluationError("to_str expects 1 argument")
            return str(args[0])
        elif name == "concat":
            if len(args) != 2:
                raise RuntimeEvaluationError("concat expects 2 arguments")
            for arg in args:
                if not isinstance(arg, str):
                    raise RuntimeEvaluationError("Input is not a string")
            try:
                return args[0] + args[1]
            except (ValueError, TypeError):  # pragma: no cover
                # seems like dead code
                raise RuntimeEvaluationError("Cannot concatenate values")
        elif name == "trim":
            if len(args) != 1:
                raise RuntimeEvaluationError("trim expects 1 argument")
            if not isinstance(args[0], str):
                raise RuntimeEvaluationError("Input is not a string")
            try:
                return args[0].strip()
            except (ValueError, TypeError):  # pragma: no cover
                # seems like dead code
                raise RuntimeEvaluationError("Cannot trim given value")
        elif name == "hasPrefix":
            if len(args) != 2:
                raise RuntimeEvaluationError("hasPrefix expects 2 arguments")
            for arg in args:
                if not isinstance(arg, str):
                    raise RuntimeEvaluationError("Input is not a string")
            try:
                return args[1].startswith(args[0])
            except (ValueError, TypeError):  # pragma: no cover
                # seems like dead code
                raise RuntimeEvaluationError("Cannot check prefix of the value")
        elif name == "hasSuffix":
            if len(args) != 2:
                raise RuntimeEvaluationError("hasSuffix expects 2 arguments")
            for arg in args:
                if not isinstance(arg, str):
                    raise RuntimeEvaluationError("Input is not a string")
            try:
                return args[1].endswith(args[0])
            except (ValueError, TypeError):  # pragma: no cover
                # seems like dead code
                raise RuntimeEvaluationError("Cannot check suffix of the value")
        elif name == "length":
            if len(args) != 1:
                raise RuntimeEvaluationError("length expects 1 argument")
            if not isinstance(args[0], str):
                raise RuntimeEvaluationError("Input is not a string")
            try:
                return len(args[0])
            except (ValueError, TypeError):  # pragma: no cover
                # seems like dead code
                raise RuntimeEvaluationError("Cannot check length of the value")
        elif name == "ifExists":
            if len(args) != 1:
                raise RuntimeEvaluationError("ifExists expects 1 argument")
            if not isinstance(args[0], str):
                raise RuntimeEvaluationError("Input is not a string")
            return _is_declared(env, args[0])
        elif name == "exit":
            if len(args) != 1:
                raise RuntimeEvaluationError("exit expects 1 argument")
            if isinstance(args[0], bool) or not isinstance(args[0], int):
                raise RuntimeEvaluationError("eixt argument must be int")
            raise _ExitSignal(args[0])
        elif name == "type":
            if len(args) != 1:
                raise RuntimeEvaluationError("type expects 1 argument")
            v = args[0]

            if v is None:
                return "null"
            if isinstance(v, bool):
                return "boolean"
            if isinstance(v, int):
                return "integer"
            if isinstance(v, float):
                return "float"
            if isinstance(v, str):
                return "string"
            if isinstance(v, FunctionStatement):
                return "function"

            return "unknown"
        else:
            stack = _env_stack(env)
            stack.append({})
            function = _get_var(stack, node.identifier_name)[0]
            if not isinstance(function, FunctionStatement):
                stack.pop()
                raise RuntimeEvaluationError(
                    "Looked for function but found another identifier instead"
                )

            if len(node.parameters) != len(function.variables):
                stack.pop()
                raise RuntimeEvaluationError(
                    "Number of parameters passed is not equal to number of function parameters"
                )
            for identifier, expression in zip(function.variables, node.parameters):
                _declare_var(stack, identifier.name, _eval(expression, env), False)
            try:
                result = _eval(function.block, stack)
                stack.pop()
                return result
            except _ReturnSignal as e:
                stack.pop()
                return e.value

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

        # bitwise
        if t == Token.BITWISE_AND:
            _check_integer_operands(left, right)
            return left & right
        if t == Token.BITWISE_OR:
            _check_integer_operands(left, right)
            return left | right
        if t == Token.BITWISE_XOR:
            _check_integer_operands(left, right)
            return left ^ right

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

    if isinstance(node, WhileStatement):
        result = None
        while bool(_eval(node.condition, env)):
            try:
                result = _eval(node.block, env)
            except _ContinueSignal:
                continue
            except _BreakSignal:
                break
        return result

    if isinstance(node, FunctionStatement):
        _declare_var(env, node.identifier.name, node, True)
        return None

    if isinstance(node, ReturnStatement):
        evaluation = _eval(node.expression, env)
        raise _ReturnSignal(evaluation)

    raise RuntimeEvaluationError(
        f"Evaluation not implemented for node type {type(node).__name__}"
    )


def evaluate(expressions: list[Expression], env: Env | None = None) -> Any:
    if env is None:
        env = [{}]

    try:
        result = None
        for expression in expressions:
            result = _eval(expression, env)
        return result
    except _ExitSignal as e:
        return e.code
    except _ReturnSignal as e:
        return e.value
    except _ContinueSignal:
        raise RuntimeEvaluationError("continue used outside loop")
    except _BreakSignal:
        raise RuntimeEvaluationError("break used outside loop")
