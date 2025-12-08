import string
from src.tokens import Token
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

    def read_number(self) -> Tuple[Token, str]:
        is_float = False

        start = self.position
        if self.ch == "-":
            self.read_char()

        while self.ch.isdigit():
            self.read_char()

        if self.ch == ".":
            if self.peek().isdigit():
                is_float = True
                self.read_char()
            else:
                raise Exception("Wrong declaration of float")

        while self.ch.isdigit():
            self.read_char()

        return Token.FLOAT if is_float else Token.INT, self.input[start : self.position]

    def next_token(self) -> Tuple[Token, str]:
        self.skip_non_tokens()

        token: Token = Token.EOF
        str_repr: str = ""

        match self.ch:
            case "=":
                if self.peek() == "=":
                    self.read_char()
                    token, str_repr = Token.EQUAL, "=="
                else:
                    token, str_repr = Token.ASSIGN, "="
            case ch if ch == "!" and self.peek() == "=":
                self.read_char()
                token, str_repr = Token.NOTEQUAL, "!="
            case "!":
                token, str_repr = Token.NOT, "!"
            case "&":
                if self.peek() == "&":
                    self.read_char()
                    token, str_repr = Token.AND, "&&"
                else:
                    token, str_repr = Token.EOF, "Unknown"
            case "|":
                if self.peek() == "|":
                    self.read_char()
                    token, str_repr = Token.OR, "||"
                else:
                    token, str_repr = Token.EOF, "Unknown"
            case ";":
                token, str_repr = Token.SEMICOLON, ";"
            case "\0":
                token, str_repr = Token.EOF, "\0"
            case ">":
                if self.peek() == "=":
                    self.read_char()
                    token, str_repr = Token.GREATEREQUAL, ">="
                else:
                    token, str_repr = Token.GREATER, ">"
            case "<":
                if self.peek() == "=":
                    self.read_char()
                    token, str_repr = Token.LESSEQUAL, "<="
                else:
                    token, str_repr = Token.LESS, "<"

            case "(":
                token, str_repr = Token.LPAREN, "("
            case ")":
                token, str_repr = Token.RPAREN, ")"
            case "{":
                token, str_repr = Token.LBRACE, "{"
            case "}":
                token, str_repr = Token.RBRACE, "}"
            case ",":
                token, str_repr = Token.COMMA, ","

            # arithmetic operators
            case "+":
                token, str_repr = Token.PLUS, "+"
            case "-":
                if self.peek().isdigit():
                    return self.read_number()
                else:
                    token, str_repr = Token.MINUS, "-"
            case "*":
                token, str_repr = Token.ASTERISK, "*"
            case "/":
                token, str_repr = Token.SLASH, "/"

            case ch if ch.isdigit() or (ch == "-" and self.peek().isdigit()):
                # integer and float literals
                return self.read_number()
            case ch if ch in ["'", '"']:
                token, str_repr = self._read_char_string()
            case ch if ch in string.ascii_letters:
                token, str_repr = self._read_identifier()
            case _:
                token, str_repr = Token.EOF, "\0"
        self.read_char()
        return token, str_repr

    def _read_char_string(self) -> Tuple[Token, str]:
        start_quote = self.ch
        start_pos = self.position
        self.read_char()

        word: str = start_quote
        while self.ch != start_quote and self.ch != "\0":
            word += self.ch
            self.read_char()
        word += self.ch

        if self.ch == "\0":
            return Token.EOF, "\0"

        if word.startswith("'") and word.endswith("'"):
            if len(word) == 2 or len(word) == 3:
                return Token.CHAR, word[1:-1]
            else:
                # This has to be error.
                return Token.EOF, "\0"

        if len(word) >= 2 and word.startswith('"') and word.endswith('"'):
            return Token.STRING, word[1:-1]

        assert False, (
            "Something went wrong in parsing `STRING` and `CHAR` token in the `Lexer`"
        )

    # takes in a word and should return a matching token, new tokens will be added over time
    def _read_identifier(self) -> Tuple[Token, str]:
        word: str = ""
        while self.peek() in string.ascii_letters or self.peek() in string.digits:
            word += self.ch
            self.read_char()
        word += self.ch
        match word:
            case "let":
                return Token.LET, word
            case "const":
                return Token.CONST, word
            case "if":
                return Token.IF, word
            case "else":
                return Token.ELSE, word
            case "for":
                return Token.FOR, word
            case "true":
                return Token.TRUE, word
            case "false":
                return Token.FALSE, word
            case "fn":
                return Token.FUNCTION, word
            case "return":
                return Token.RETURN, word
            case _:
                return Token.IDENTIFIER, word

    def __repr__(self):
        return f"{type(self).__name__}()"
