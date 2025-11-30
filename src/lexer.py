from token import Token
from typing import Tuple


class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.position: int = 0
        self.read_position: int = 0
        self.line_number: int = 1
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

    def skip_whitespace(self) -> bool:
        while self.ch in ("\n", "\t", "\r", " "):
            self.read_char()

    def skip_singleline_comment(self):
        while self.ch not in ("\0", "\n"):
            self.read_char()

    def skip_non_tokens(self):
        while True:
            self.skip_whitespace()
            match self.ch:
                case "#":
                    self.skip_singleline_comment()
                    self.skip_whitespace()
                case "/":
                    if self.peek() == "/":
                        self.read_char()
                        self.skip_singleline_comment()
                        self.skip_whitespace()
                case _:
                    return

    def next_token(self) -> Tuple[Token, str]:
        self.skip_non_tokens()
        splitting_characters: set = {" ", "\n"}
        identifier_enders: set = {";", "\0", "="}

        if self.ch == "\0":
            return Token.EOF, "\0"

        if self.ch in identifier_enders:
            token, word = self._match_token(self.ch)
            self.read_char()
            return token, word

        word: str = ""
        while self.ch not in splitting_characters and self.ch not in identifier_enders:
            word += self.ch
            self.read_char()
        return self._match_token(word)

    # takes in a word and should return a matching token, new tokens will be added over time
    def _match_token(self, word: str) -> Tuple[Token, str]:
        match word:
            case "let":
                return Token.LET, word
            case "const":
                return Token.CONST, word
            case "=":
                return Token.ASSIGN, word
            case ";":
                return Token.SEMICOLON, word
            case "\0":
                return Token.EOF, word
            case word if len(word) >= 2 and word.startswith("'") and word.endswith("'"):
                return Token.CHAR, word[1:-1]
            case word if len(word) >= 2 and word.startswith('"') and word.endswith('"'):
                return Token.STRING, word[1:-1]
            case _:
                return Token.IDENTIFIER, word

    def __repr__(self):
        return f"{type(self).__name__}()"
