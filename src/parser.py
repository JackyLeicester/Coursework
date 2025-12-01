from lexer import Lexer
from token import Token
from collections.abc import Callable
import sys


class Expression:
    pass


class ExpressionStatement(Expression):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression


class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value


class BlockStatement:
    pass


class IfExpression:
    def __init__(
        self,
        condition: Expression,
        consequence: BlockStatement,
        alternative: BlockStatement,
    ) -> None:
        self.token = Token.IF
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f"{type(self).__name__} {self.__dict__}"


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token, self.curr_str = self.lexer.next_token()
        self.next_token, self.next_str = self.lexer.next_token()
        self.errors = []
        self.variables = dict()
        self.prefix_parse_fns: dict[Token, Callable[[], [Expression]]] = dict()
        self.infix_parse_fns: dict[Token, Callable[[Expression], [Expression]]] = dict()

        self._register_prefix_fn(Token.IDENTIFIER, self.parse_identifier)
        self._register_prefix_fn(Token.IF, self.parse_if_expression)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def _register_prefix_fn(self, token: Token, fn: Callable[[], [Expression]]) -> None:
        self.prefix_parse_fns[token] = fn

    def _register_infix_fn(
        self, token: Token, fn: Callable[[Expression], [Expression]]
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
                case _:
                    self.parse_expression_statement()
            self._next_token()

    def parse_expression_statement(self) -> ExpressionStatement:
        token, str_repr = self.curr_token, self.curr_str
        expression = self.parse_expression()
        if self._peek_token_is(Token.SEMICOLON):
            self.next_token()
        return ExpressionStatement(token, expression)

    def parse_expression(self) -> Expression:
        prefix_parse_fn = self.prefix_parse_fns[self.curr_token]
        if prefix_parse_fn is None:
            return None
        left_exp: Expression = prefix_parse_fn()
        return left_exp

    def parse_identifier(self) -> Identifier:
        return Identifier(self.curr_token, self.curr_str)

    def parse_if_expression(self) -> IfExpression | None:
        self._next_token()
        condition = self.parse_expression()
        if self.next_token != Token.LPAREN:
            return None
        consequence = self.parse_block_statement()
        if self.next_token == Token.ELSE:
            alternative = self.parse_block_statement()
        return IfExpression(condition, consequence, alternative)

    def parse_expression(self) -> Expression | None:
        pass

    def parse_block_statement(self) -> BlockStatement | None:
        pass

    def _call_syntax_error(self, expected_tokens: list[str], actual_token: str) -> None:
        message: str = f"SYNTAX ERROR: expected tokens: "
        message += "".join([token + " " for token in expected_tokens])
        message += (
            "\n" + f"actual_token: {actual_token} at line: {self.lex.line_number}"
        )
        sys.exit(message)
