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

    def next_token(self) -> Token:
        splitting_characters: set = {' ', '\n'}
        while self.ch in splitting_characters:
            self.read_char()

        if self.ch == '\0':
            return Token.EOF
        
        word: str = ""
        while self.ch not in splitting_characters and self.ch != '\0':
            word += self.ch
            self.read_char()
        return self.match_token(word)

    # takes in a word and should return a matching token, new tokens will be added over time
    def match_token(self, word: str)->Token:
        print(f"trying to process word: {word} into token")
        pass
         
    def __repr__(self):
        return f"{type(self).__name__}()"

    def call_lexical_error(self, word: str, line_number: int)->None:
        message: str = f"token {word} does not match any word in the language at line: {line_number}"
        sys.exit(message)