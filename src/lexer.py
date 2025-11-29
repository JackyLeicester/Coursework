from token import Token


class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.position: int = 0
        self.read_position: int = 0
        self.ch = "\0"
        self.read_char()

    def read_char(self) -> None:
        if self.read_position >= len(self.input):
            self.ch = "\0"
        else:
            self.ch = self.input[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def peek(self):
        if self.read_position >= len(self.input):
            return "\0"
        return self.input[self.read_position]

    def skip_whiteSpace(self):
        while self.ch in ("\n", "\t", "\r", " "):
            self.read_char()

    def skip_singleLine_comment(self):
        while self.ch not in ("\0", "\n"):
            self.read_char()

    def next_token(self) -> Token:
        self.skip_whiteSpace()

        if self.ch == "#":
            self.skip_singleLine_comment()
            return self.next_token()

        if self.ch == "/" and self.peek() == "/":
            self.read_char()
            self.skip_singleLine_comment()
            return self.next_token()

        if self.ch == "\0":
            return Token.Eof

        self.read_char()
        return self.next_token()

    def __repr__(self):
        return f"{type(self).__name__}()"
