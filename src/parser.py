from src.lexer import Lexer
from src.tokens import Token
from typing import Dict, List, Tuple
from collections.abc import Callable
from enum import Enum, auto
import sys


class Expression:
    pass


class ExpressionStatement(Expression):
    def __init__(self, token: Token, expression: Expression | None):
        self.token = token
        self.expression = expression


class InfixExpression(Expression):
    def __init__(self, lhs: Expression, operation: Token, rhs: Expression):
        self.lhs = lhs
        self.operation = operation
        self.rhs = rhs


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression | None):
        self.token = token
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.operator}{self.right})"


class Identifier(Expression):
    def __init__(self, token: Token, name: str, read_only: bool = False):
        self.token = token
        self.name = name
        self.value = "null"
        self.read_only = read_only

    def get(self):
        return self.value

    def set(self, value):
        if self.read_only:
            # call logical errors once that is complete
            raise ZeroDivisionError
        self.value = value


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value
    def __repr__(self):
        return f"{self.value}"


class LetStatement(Expression):
    def __init__(self, identifier: Identifier, expression: Expression):
        self.identifier = identifier
        self.expression = expression


class ConstStatement(Expression):
    def __init__(self, identifier: Identifier, expression: Expression):
        self.identifier = identifier
        self.expression = expression


class BlockStatement(Expression):
    def __init__(self, statements: List[Expression]):
        self.statements: List[Expression] = statements


class IfExpression(Expression):
    def __init__(
        self,
        condition: Expression | None,
        consequence: BlockStatement | None,
        alternative: BlockStatement | None,
    ) -> None:
        self.token = Token.IF
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f"{type(self).__name__} {self.__dict__}"


class FunctionStatement(Expression):
    def __init__(self, variables: List[Identifier], block: BlockStatement):
        self.variables = variables
        self.block = block


class ForStatement:
    def __init__(
        self,
        initialization: Expression,
        condition: Expression,
        increment: Expression,
        block: BlockStatement,
    ):
        self.token = Token.FOR
        self.initialization = initialization
        self.condition = condition
        self.increment = increment
        self.block = block

    def __repr__(self):
        return f"{type(self).__name__} {self.__dict__}"


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token, self.curr_str = self.lexer.next_token()
        self.next_token, self.next_str = self.lexer.next_token()
        self.errors = []

        self.symbols: Dict[str, object] = dict()
        self.prefix_parse_fns: dict[Token, Callable[[], Expression | None]] = dict()
        self.infix_parse_fns: dict[Token, Callable[[Expression], Expression | None]] = (
            dict()
        )

        self._register_prefix_fn(Token.IDENTIFIER, self.parse_identifier)
        self._register_prefix_fn(Token.IF, self.parse_if_expression)
        self._register_prefix_fn(Token.NOT, self.parse_prefix_expression)
        self._register_prefix_fn(Token.TRUE, self.parse_boolean)
        self._register_prefix_fn(Token.FALSE, self.parse_boolean)
        self._register_prefix_fn(Token.FUNCTION, self.parse_function_statement)
        self._register_prefix_fn(Token.LET, self.parse_let_statement)
        self._register_prefix_fn(Token.CONST, self.parse_const_statement)

        self._register_prefix_fn(Token.INT, self.parce_number_literal)
        self._register_prefix_fn(Token.FLOAT, self.parce_number_literal)

        for token in [
            Token.EQUAL,
            Token.NOTEQUAL,
            Token.LESS,
            Token.LESSEQUAL,
            Token.GREATER,
            Token.GREATEREQUAL,
            Token.AND,
            Token.OR,
        ]:
            self._register_infix_fn(token, self.parse_infix_expression)

        # arithmetic operator
        self._register_infix_fn(Token.PLUS, self.parse_infix_expression)
        self._register_infix_fn(Token.MINUS, self.parse_infix_expression)
        self._register_infix_fn(Token.ASTERISK, self.parse_infix_expression)
        self._register_infix_fn(Token.SLASH, self.parse_infix_expression)

        self._register_prefix_fn(Token.FOR, self.parse_for_statement)
        self._register_prefix_fn(Token.LPAREN, self.parse_paren)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def _register_prefix_fn(
        self, token: Token, fn: Callable[[], Expression | None]
    ) -> None:
        self.prefix_parse_fns[token] = fn

    def _register_infix_fn(
        self, token: Token, fn: Callable[[Expression], Expression | None]
    ) -> None:
        self.infix_parse_fns[token] = fn

    def _next_token(self) -> None:
        self.curr_token = self.next_token
        self.curr_str = self.next_str
        self.next_token, self.next_str = self.lexer.next_token()

    def _peek_token_is(self, token: Token) -> bool:
        return self.next_token == token

    def run(self) -> None:
        while self.curr_token != Token.EOF:
            match self.curr_token:
                case Token.IF:
                    print(self.parse_if_expression())
                case Token.FOR:
                    print(self.parse_for_statement())
                case _:
                    self.parse_expression_statement()
            self._next_token()

    def parse_function_statement(self) -> FunctionStatement:
        self._accept_token(Token.FUNCTION)
        identifier: Identifier = self.parse_identifier()
        self._accept_token(Token.LPAREN)
        identifiers: List[Identifier] = []
        while self.next_token == Token.IDENTIFIER:
            identifier: Identifier = self.parse_identifier()
            identifiers.append(identifier)
        self._accept_token(Token.RPAREN)
        block = self.parse_block_statement()
        fn: FunctionStatement = FunctionStatement(identifiers, block)
        return fn

    def parse_let_statement(self) -> LetStatement:
        self._accept_token(Token.LET)
        identifier: Identifier = self.parse_identifier()
        # there is a better option here
        self._accept_token(Token.IDENTIFIER)
        self._accept_token(Token.ASSIGN)
        expression: Expression = self.parse_expression()
        self._accept_token(Token.LITERAL)
        statement: LetStatement = LetStatement(identifier, expression)
        return statement

    def parse_const_statement(self) -> ConstStatement:
        self._accept_token(Token.CONST)
        identifier: Identifier = self.parse_identifier()
        self._accept_token(Token.ASSIGN)
        expression: Expression = self.parse_expression()
        statement: ConstStatement = ConstStatement(identifier, expression)
        return statement

    def parse_expression_statement(self) -> ExpressionStatement:
        token, str_repr = self.curr_token, self.curr_str
        expression = self.parse_expression()
        if self._peek_token_is(Token.SEMICOLON):
            self._next_token()
        return ExpressionStatement(token, expression)

    def parse_expression(
        self, precedence: int = Token.LOWEST_PRECEDENCE
    ) -> Expression | None:
        prefix_fn = self.prefix_parse_fns.get(self.curr_token)
        if prefix_fn is None:
            return None

        left_exp = prefix_fn()
        if left_exp is None:
            return None

        left_expr: Expression = left_exp

        while (
            self.next_token != Token.SEMICOLON and precedence < self._peek_precedence()
        ):
            infix_fn = self.infix_parse_fns.get(self.next_token)
            if infix_fn is None:
                return left_expr

            self._next_token()
            left_expr = infix_fn(left_expr)  # type: ignore[arg-type]

        return left_expr

    def parse_infix_expression(self, lhs: Expression) -> InfixExpression | None:
        token, str_repr = self.curr_token, self.curr_str
        precedence = self._curr_precedence()
        self._next_token()

        rhs = self.parse_expression(precedence)

        if rhs is None:
            return None
        return InfixExpression(lhs, token, rhs)

    def _peek_precedence(self) -> int:
        return self.next_token or Token.LOWEST_PRECEDENCE

    def _curr_precedence(self) -> int:
        return self.curr_token or Token.LOWEST_PRECEDENCE

    def parse_prefix_expression(self) -> PrefixExpression:
        token, operator = self.curr_token, self.curr_str
        self._next_token()

        right = self.parse_expression(7)
        return PrefixExpression(token, operator, right)

    def parse_boolean(self) -> Identifier:
        return Identifier(self.curr_token, self.curr_str)

    def parse_identifier(self) -> Identifier:
        return Identifier(self.curr_token, self.curr_str, self)

    def parce_number_literal(self) -> IntegerLiteral | None:
        return IntegerLiteral(self.curr_token, self.curr_str)

    def parse_if_expression(self) -> IfExpression | None:
        self._next_token()
        condition = self.parse_expression()
        if self.next_token != Token.LPAREN:
            return None
        consequence = self.parse_block_statement()
        alternative = None
        if self.next_token == Token.ELSE:
            alternative = self.parse_block_statement()
        return IfExpression(condition, consequence, alternative)

    def parse_for_statement(self) -> ForStatement | None:
        self._next_token()
        if not self._peek_token_is(Token.LPAREN):
            return None
        initialization = self.parse_expression()
        if not self._peek_token_is(Token.SEMICOLON):
            return None
        condition = self.parse_expression()
        if not self._peek_token_is(Token.SEMICOLON):
            return None
        increment = self.parse_expression()
        if not self._peek_token_is(Token.RPAREN):
            return None
        block = self.parse_block_statement()
        return ForStatement(initialization, condition, increment, block)

    def parse_paren(self) -> Expression | None:
        self._next_token()

        expr = self.parse_expression(Token.LOWEST_PRECEDENCE)
        if expr is None:
            return None

        if not self._peek_token_is(Token.RPAREN):
            return None

        self._next_token()
        return expr

    def parse_block_statement(self) -> BlockStatement | None:
        self._accept_token(Token.LBRACKETS)
        statements: List[Expression] = []
        while self.curr_token != Token.RBRACKETS:
            statement: Expression = self.parse_expression_statement()
            statements.append(statement)
        self._accept_token(Token.RBRACKETS)
        block: BlockStatement = BlockStatement(statements)
        return block

    def _get_token_name(self, token: Token) -> str:
        for name, value in Token.__dict__.items():
            if value == token:
                return name
        return "NOT A TOKEN"

    def _call_syntax_error(
        self, expected_tokens: list[Token], actual_token: Token, token_text: str
    ) -> None:
        message: str = f"SYNTAX ERROR: expected tokens: "
        message += "".join(
            [self._get_token_name(token) + " " for token in expected_tokens]
        )
        message += (
            "\n"
            + f"actual_token: {self._get_token_name(actual_token)} {token_text} at line: {self.lexer.line_number}"
        )
        raise Exception(message)

    def _accept_token(self, token: Token):
        if self.curr_token != token:
            self._call_syntax_error([token], self.curr_token, self.curr_str)
        self._next_token()
