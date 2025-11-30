from token import Token
from typing import Tuple
import sys

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

    def skip_whitespace(self):
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
                    return self.next_token()
                case "/":
                    if self.peek() == "/":
                        self.read_char()
                        self.skip_singleline_comment()
                    else:
                        self.read_char()
                case _:
                    return

    def next_token(self) -> Tuple[Token, str]:
        self.skip_non_tokens()
        splitting_characters: set = {' ', '\n'}
        identifier_enders: set = {';', '\0', "="}

        if self.ch == "\0":
            return Token.EOF, '\0'

        if self.ch in identifier_enders:
            output: Token = self.match_token(self.ch)
            word: str = self.ch
            self.read_char()
            return output, word
        
        word: str = ""
        while self.ch not in splitting_characters and self.ch not in identifier_enders:
            word += self.ch
            self.read_char()
        return self.match_token(word), word

    # takes in a word and should return a matching token, new tokens will be added over time
    def match_token(self, word: str)->Token:
        match(word):
            case "let":
                return Token.LET
            case "=":
                return Token.ASSIGN
            case ";":
                return Token.SEMICOLON
            case "\0":
                return Token.EOF
            # assuming this is the default case in python
        if self._is_literal(word):
            return Token.LITERAL
        else:
            return Token.IDENTIFIER

    def _is_literal(self, word: str) -> bool:
        if len(word) >= 2:
            if word[0] == '"' and word[-1] == '"':
                return True
        return word.isnumeric()
         
    def __repr__(self):
        return f"{type(self).__name__}()"

    def call_error(self, word: str, line_number: int)->None:
        message: str = f"token {word} does not match any word in the language at line: {line_number}"
        sys.exit(message)
