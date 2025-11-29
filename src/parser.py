from lexer import Lexer
from token import Token
from functools import partial

import sys

class Parser:
    lex: Lexer
    current_token: Token
    variables: dict
    current_token_string: str
    def __init__(self, lex:Lexer):
        self.lex = lex
        self._next_token()
        self.variables = dict()
        self.current_token_string = ""

    def __repr__(self):
        return f"""{type(self).__name__}() 
            {self.variables}
        """
    
    def parse_file(self)->None:
        # placeholder code
        self._program()

    def _accept_token(self, token: Token):
        if self.current_token != token:
            self.call_syntax_error([], self.current_token, -1)
        self._next_token()
    
    def _next_token(self):
        next_token: tuple = self.lex.next_token()
        self.current_token_string = next_token[0]
        self.current_token = next_token[1]

    def call_syntax_error(self, expected_tokens: list[str], actual_token: str, line_number: int)->None:
        message: str = f"SYNTAX ERROR: expected tokens: "
        message += "".join([token + " " for token in expected_tokens])
        message += "\n" + f"actual_token: {actual_token} at line: {line_number}"
        sys.exit(message)

    def call_runtime_error(self, message: str, line_number: int):
        message: str = f"RUNTIME ERROR: {message} at line: {line_number}"
        sys.exit(message)
    
    def _program(self) -> None:
        while self.current_token != Token.EOF:
            self._statement()
    
    def _statement(self) -> None:
        print('current token', self.current_token)
        # python does not do enum matching so we need ifs
        if self.current_token == Token.LET:
            self._intialization()
        else:
            self.call_syntax_error([';'], self.current_token, -1)    
        self._accept_token(Token.SEMICOLON)

    def _intialization(self) -> None:
        print('initializing')
        self._variable_decl()

    def _variable_decl(self) -> None:
        self._accept_token(Token.LET)
        assignment_function: partial = self._lhs_var_decl()
        self._accept_token(Token.ASSIGN)
        value = self._expression()
        assignment_function(value=value)

    #needs to return the value of the expression
    def _expression(self):
        # placeholder that is ucrrently hard coded to identifier
        if self.current_token == Token.LITERAL:
            token = self.current_token_string
            self._accept_token(Token.LITERAL)
            return token
        elif self.current_token == Token.IDENTIFIER:
            token = self.current_token_string
            self._accept_token(Token.IDENTIFIER)
            return token
        
    def _lhs_var_decl(self) -> partial:
        # this will need to handle indexes in the future too, we probably need lookahead 1
        if self.current_token == Token.IDENTIFIER:
            partial_function: partial = partial(
                self._set_variable, 
                variable_name=self.current_token_string
            )
            self._accept_token(Token.IDENTIFIER)
            return partial_function
        else:
            self.call_syntax_error(["identifier"], self.current_token_string, -1)

    def _set_variable(self, variable_name: str, value) -> None:
        self.variables[variable_name] = value

    def _index(self) -> None:
        #placeholder
        pass
    