from lexer import Lexer
from token import Token
import sys


class Expression:
    pass


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

    def __repr__(self):
        return f"{type(self).__name__}()"

    def _next_token(self) -> None:
        self.curr_token = self.next_token
        self.curr_str = self.next_str
        self.next_token, self.next_str = self.lexer.next_token()

    def run(self) -> None:
        while self.curr_token != Token.EOF:
            match self.curr_token:
                case Token.IF:
                    print(self.parse_if_expression())
                case Token.IDENTIFIER:
                    self.parse_identifier()
                case _:
                    print(self.curr_token, self.curr_str)
            self._next_token()

    def parse_identifier(self) -> Identifier:
        return Identifier(self.curr_token, self.curr_str)

    def parse_if_expression(self) -> IfExpression | None:
        self._next_token()
        expression = self.parse_expression()
        if self.next_token != Token.LPAREN:
            return None
        consequence = self.parse_block_statement()
        if self.next_token == Token.ELSE:
            alternative = self.parse_block_statement()
        if_expr = IfExpression(expression, consequence, alternative)
        return if_expr

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
