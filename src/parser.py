from lexer import Lexer
from token import Token


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.next_token()
        self.next_token = self.lexer.next_token()
        self.errors = []

    def __repr__(self):
        return f"{type(self).__name__}()"

    def _next_token(self) -> None:
        self.curr_token = self.next_token
        self.next_token = self.lexer.next_token()

    def run(self) -> None:
        while self.curr_token != Token.EOF:
            self._next_token()
