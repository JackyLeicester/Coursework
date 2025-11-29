from token import Token
import sys

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

    def skip_whitespace(self):
        while self.ch in ("\n", "\t", "\r", " "):
            self.read_char()

    def skip_singleline_comment(self):
        while self.ch not in ("\0", "\n"):
            self.read_char()

    def next_token(self) -> Token:
        self.skip_whitespace()

        if self.ch == "\0":
            return Token.EoF

        match self.ch:
            case "#":
                self.skip_singleline_comment()
                return self.next_token()

            case "/":
                if self.peek() == "/":
                    self.read_char()
                    self.skip_singleline_comment()
                    return self.next_token()
                else:
                    self.read_char()
                    return self.next_token()

            case _:
                self.read_char()
                return self.next_token()

    # takes in a word and should return a matching token, new tokens will be added over time
    def match_token(self, word: str)->Token:
        print(f"trying to process word: {word} into token")
        pass
         
    def __repr__(self):
        return f"{type(self).__name__}()"

    def call_lexical_error(self, word: str, line_number: int)->None:
        message: str = f"token {word} does not match any word in the language at line: {line_number}"
        sys.exit(message)