from dataclasses import dataclass

from .lexer import Lexer
from .tokens import Token
from typing import Dict, List
from collections.abc import Callable


class IncorrectSyntax(Exception):
    """
    This should be named 'SyntaxError' but it clashes with the built-in
    exception of python. Hence, 'IncorrectSyntax' is chosen as an
    alternative name.
    """

    def __init__(self, message: str):
        self.message = message


class Expression:
    pass


@dataclass
class ExpressionStatement(Expression):
    token: Token
    expression: Expression


@dataclass
class InfixExpression(Expression):
    lhs: Expression
    operation: Token
    rhs: Expression


@dataclass
class PrefixExpression(Expression):
    token: Token
    right: Expression


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class IntegerLiteral(Expression):
    value: int


@dataclass
class FloatLiteral(Expression):
    value: float


@dataclass
class BooleanLiteral(Expression):
    literal: bool


@dataclass
class LetStatement(Expression):
    identifier: Identifier
    expression: Expression


class ConstStatement(Expression):
    def __init__(self, identifier: Identifier, expression: Expression):
        self.identifier = identifier
        self.expression = expression


class AssignExpression(Expression):
    def __init__(self, lhs: Expression, rhs: Expression):
        self.lhs = lhs
        self.token = Token.ASSIGN
        self.rhs = rhs


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
    def __init__(
        self, identifier: Identifier, variables: List[Identifier], block: BlockStatement
    ):
        self.identifier = identifier
        self.variables = variables
        self.block = block


class ReturnStatement(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression


class CallExpression(Expression):
    def __init__(self, identifier_name: str, parameters: List[Expression]):
        self.identifier_name = identifier_name
        self.parameters = parameters


class ForStatement(Expression):
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


@dataclass
class ContinueStatement(Expression):
    pass


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

        self._register_prefix_fn(
            Token.IDENTIFIER, self.parse_identifier_or_callexpression
        )
        self._register_prefix_fn(Token.IF, self.parse_if_expression)
        self._register_prefix_fn(Token.NOT, self.parse_prefix_expression)
        self._register_prefix_fn(Token.TRUE, self.parse_boolean)
        self._register_prefix_fn(Token.FALSE, self.parse_boolean)
        self._register_prefix_fn(Token.FUNCTION, self.parse_function_statement)
        self._register_prefix_fn(Token.LET, self.parse_let_statement)
        self._register_prefix_fn(Token.CONST, self.parse_const_statement)
        self._register_prefix_fn(Token.RETURN, self.parse_return_statement)

        self._register_prefix_fn(Token.INT, self.parse_number_literal)
        self._register_prefix_fn(Token.FLOAT, self.parse_number_literal)

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
        self._register_prefix_fn(Token.CONTINUE, self.parse_continue_statement)
        self._register_prefix_fn(Token.LPAREN, self.parse_paren)
        self._register_prefix_fn(Token.LBRACE, self.parse_block_statement)

        self._register_infix_fn(Token.ASSIGN, self.parse_assignment_expression)

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

    def run(self) -> [Expression]:
        expressions = []
        while self.curr_token != Token.EOF:
            expressions.append(self.parse_expression())
            self._next_token()
        return expressions

    def parse_function_statement(self) -> FunctionStatement:
        self._accept_token(Token.FUNCTION)
        identifier: Identifier = self.parse_identifier()
        self._accept_token(Token.LPAREN)
        identifiers: List[Identifier] = []
        while self.curr_token == Token.IDENTIFIER:
            identifier: Identifier = self.parse_identifier_or_callexpression()
            identifiers.append(identifier)
        self._accept_token(Token.RPAREN)
        block = self.parse_block_statement()
        fn: FunctionStatement = FunctionStatement(identifier, identifiers, block)
        self._accept_token(Token.SEMICOLON)
        return fn

    def parse_return_statement(self) -> ReturnStatement:
        self._accept_token(Token.RETURN)
        expression: Expression = self.parse_expression()
        self._accept_token(Token.SEMICOLON)
        return ReturnStatement(expression)

    def parse_let_statement(self) -> LetStatement:
        self._accept_token(Token.LET)
        identifier: Identifier = self.parse_identifier()
        self._accept_token(Token.ASSIGN)
        expression: Expression = self.parse_expression()
        statement: LetStatement = LetStatement(identifier, expression)
        self._accept_token(Token.SEMICOLON)
        return statement

    def parse_const_statement(self) -> ConstStatement:
        self._accept_token(Token.CONST)
        identifier: Identifier = self.parse_identifier()
        self._accept_token(Token.ASSIGN)
        expression: Expression = self.parse_expression()
        statement: ConstStatement = ConstStatement(identifier, expression)
        # workaround for expressions not moving forwards
        self._accept_token(Token.SEMICOLON)
        return statement

    def parse_assignment_expression(self, lhs: Expression) -> AssignExpression:
        self._accept_token(Token.ASSIGN)
        rhs = self.parse_expression()
        return AssignExpression(lhs, rhs)

    def parse_expression_statement(self) -> ExpressionStatement:
        token, _ = self.curr_token, self.curr_str
        expression = self.parse_expression()
        return ExpressionStatement(token, expression)

    def parse_expression(
        self, precedence: int = Token.LOWEST_PRECEDENCE
    ) -> Expression | None:
        prefix_fn = self.prefix_parse_fns.get(self.curr_token)
        if prefix_fn is None:
            raise IncorrectSyntax(
                "Illegal token start"
            )

        left_exp = prefix_fn()
        if left_exp is None:
            return None

        left_expr: Expression = left_exp

        while (
            self.next_token != Token.SEMICOLON and precedence < self._curr_precedence()
        ):
            infix_fn = self.infix_parse_fns.get(self.curr_token)
            if infix_fn is None:
                return left_expr
            left_expr = infix_fn(left_expr)

        return left_expr

    def parse_infix_expression(self, lhs: Expression) -> InfixExpression | None:
        operator = self.curr_token
        precedence = self._curr_precedence()
        self._next_token()

        rhs = self.parse_expression(precedence)

        if rhs is None:
            return None

        return InfixExpression(lhs, operator, rhs)

    def _peek_precedence(self) -> int:
        return self.next_token or Token.LOWEST_PRECEDENCE

    def _curr_precedence(self) -> int:
        return self.curr_token or Token.LOWEST_PRECEDENCE

    def parse_prefix_expression(self) -> PrefixExpression:
        token = self.curr_token
        precedence = self._curr_precedence()
        self._next_token()
        right = self.parse_expression(precedence)
        return PrefixExpression(token, right)

    def parse_boolean(self) -> BooleanLiteral:
        literal = BooleanLiteral(self.curr_str == "true")
        self._next_token()
        return literal

    def parse_identifier_or_callexpression(self) -> Identifier | CallExpression:
        if self.next_token == Token.LPAREN:
            return self.parse_callexpression()
        else:
            return self.parse_identifier()

    def parse_callexpression(self) -> CallExpression:
        name: str = self.curr_str
        self._accept_token(Token.IDENTIFIER)
        self._accept_token(Token.LPAREN)
        parameters: List[Expression] = []
        if self.curr_token != Token.RPAREN:
            parameters.append(self.parse_expression())
            while self.curr_token != Token.RPAREN:
                self._accept_token(Token.COMMA)
                parameters.append(self.parse_expression())
        self._accept_token(Token.RPAREN)
        self._accept_token(Token.SEMICOLON)
        return CallExpression(name, parameters)

    def parse_identifier(self) -> Identifier:
        identifier = Identifier(self.curr_str)
        self._accept_token(Token.IDENTIFIER)
        return identifier

    def parse_number_literal(self) -> IntegerLiteral | FloatLiteral:
        literal = (
            IntegerLiteral(int(self.curr_str))
            if self.curr_token == Token.INT
            else FloatLiteral(float(self.curr_str))
        )
        self._next_token()
        return literal

    def parse_if_expression(self) -> IfExpression | None:
        self._next_token()
        condition = self.parse_expression()
        consequence = self.parse_block_statement()
        alternative = None
        if self.curr_token == Token.ELSE:
            self._accept_token(Token.ELSE)
            alternative = self.parse_block_statement()
        return IfExpression(condition, consequence, alternative)

    def parse_for_statement(self) -> ForStatement | None:
        self._accept_token(Token.FOR)
        self._accept_token(Token.LPAREN)

        initialization = self.parse_expression()
        self._accept_token(Token.SEMICOLON)

        condition = self.parse_expression()
        self._accept_token(Token.SEMICOLON)

        increment = self.parse_expression()
        self._accept_token(Token.RPAREN)

        block = self.parse_block_statement()
        return ForStatement(initialization, condition, increment, block)

    def parse_continue_statement(self) -> ContinueStatement:
        self._accept_token(Token.CONTINUE)
        self._accept_token(Token.SEMICOLON)
        return ContinueStatement()

    def parse_paren(self) -> Expression | None:
        self._next_token()

        expr = self.parse_expression(Token.LOWEST_PRECEDENCE)
        if expr is None:
            return None

        if self.curr_token != Token.RPAREN:
            return None

        self._next_token()
        return expr

    def parse_block_statement(self) -> BlockStatement | None:
        self._accept_token(Token.LBRACE)
        statements: List[Expression] = []
        while self.curr_token != Token.RBRACE and self.curr_token != Token.EOF:
            statement: Expression = self.parse_expression_statement()
            statements.append(statement)
        self._accept_token(Token.RBRACE)
        block: BlockStatement = BlockStatement(statements)
        return block

    def _syntax_error(
        self, expected_tokens: list[Token], actual_token: Token, token_text: str
    ) -> None:
        message: str = "SYNTAX ERROR: expected tokens: "
        message += "".join([str(token) + " " for token in expected_tokens])
        message += (
            "\n"
            + f"actual tokens: {str(actual_token)} {token_text} at line: {self.lexer.line_number}"
        )
        raise IncorrectSyntax(message)

    def _accept_token(self, token: Token):
        if self.curr_token != token:
            self._syntax_error([token], self.curr_token, self.curr_str)
        self._next_token()
