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
