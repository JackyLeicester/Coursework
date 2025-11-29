from lexer import Lexer
from token import Token
class Parser:
    lex: Lexer
    current_token: Token
    def __init__(self, lex:Lexer):
        self.lex = lex
        self.current_token = self.lex.next_token()

    def parse_file(self)->None:
        # placeholder code
        while self.current_token != Token.EOF:
            self.accept_token()
            
    def accept_token(self):
        self.current_token = self.lex.next_token()
    
    def __repr__(self):
        return f"{type(self).__name__}()"


    def call_syntax_erorr(self, expected_tokens: list[str], actual_token: str, line_number: int)->None:
        message: str = "SYNTAX ERROR: expected tokens: ".join([token + " " for token in expected_tokens])
        message += "\n" + f"actual_token: {actual_token} at line: {line_number}"
        sys.exit(message)

    def call_runtime_error(self, message: str, line_number: int):
        message: str = f"RUNTIME ERROR: {message} at line: {line_number}"
        sys.exit(message)