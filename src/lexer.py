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

    # returns first the type of the token followed by the string version
    def next_token(self) -> tuple:
        splitting_characters: set = {' ', '\n'}
        # these are used to end tokens and also act as tokens on their own
        identifier_enders: set = {';', '\0', "="}

        while self.ch in splitting_characters:
            self.read_char()
        
        if self.ch in identifier_enders:
            print('is a single char')
            output: Token = self.match_token(self.ch)
            word: str = self.ch
            self.read_char()
            return word, output

        if self.ch == '\0':
            return Token.EOF
        
        word: str = ""
        while self.ch not in splitting_characters and self.ch not in identifier_enders:
            word += self.ch
            self.read_char()
        return word, self.match_token(word)

    # takes in a word and should return a matching token, new tokens will be added over time
    def match_token(self, word: str)->Token:
        print(f"trying to process word: {word} into token")
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