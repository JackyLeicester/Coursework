from lexer import Lexer
from token import Token
from typing import Dict
import sys


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token, self.curr_str = self.lexer.next_token()
        self.next_token, self.next_str = self.lexer.next_token()
        self.errors = []
        self.variables: Dict[str, Variable]

    def __repr__(self):
        return f"{type(self).__name__}()"

    def _next_token(self) -> None:
        self.curr_token = self.next_token
        self.curr_str = self.next_str
        self.next_token, self.next_str = self.lexer.next_token()

    def run(self) -> None:
        while self.curr_token != Token.EOF:
            print(self.curr_token, self.curr_str)
            self._next_token()

    def _call_syntax_error(self, expected_tokens: list[str], actual_token: str) -> None:
        message: str = f"SYNTAX ERROR: expected tokens: "
        message += "".join([token + " " for token in expected_tokens])
        message += (
            "\n" + f"actual_token: {actual_token} at line: {self.lex.line_number}"
        )
        sys.exit(message)


class Variable:
    def __init__(self, value, parser: Parser, read_only=False):
        self.read_only = read_only
        self.parser = parser
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        if self.read_only:
            # call logical errors once that is complete
            return
        self.value = value
