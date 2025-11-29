from lexer import Lexer
from token import Token

import sys
import functools

class Parser:
    lex: Lexer
    current_token: Token
    variables: dict
    current_token_string: str
    def __init__(self, lex:Lexer):
        self.lex = lex
        self.current_token = self.lex.next_token()
        self.variables = dict()
        self.current_token_string = ""

    def parse_file(self)->None:
        # placeholder code
        while self.current_token != Token.EOF:
            self.accept_token()
            
    def accept_token(self):
        next_token: tuple = self.lex.next_token()
        self.current_token, self.current_token_string = next_token

    def call_syntax_erorr(self, expected_tokens: list[str], actual_token: str, line_number: int)->None:
        message: str = "SYNTAX ERROR: expected tokens: ".join([token + " " for token in expected_tokens])
        message += "\n" + f"actual_token: {actual_token} at line: {line_number}"
        sys.exit(message)

    def call_runtime_error(self, message: str, line_number: int):
        message: str = f"RUNTIME ERROR: {message} at line: {line_number}"
        sys.exit(message)
    
    def __repr__(self):
        return f"{type(self).__name__}()"
    
    def _intialization(self) -> None:
        pass

    def _variable_decl(self) -> None:
        self._lhs_var_decl()

    def _lhs_var_decl(self) -> functools.partial:
        # this will need to handle indexes in the future too, we probably need lookahead 1
        if self.current_token == Token.IDENTIFIER:
            return functools.partial(self._set_variable, variable_name=self.current_token_string)
        
    def _set_variable(self, variable_name: int, value) -> None:
        self.variables[variable_name] = value

    def _index(self) -> None:
        pass
    