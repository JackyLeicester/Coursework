from lexer import Lexer
from token import Token
from typing import Dict, List, Tuple
from collections.abc import Callable
from enum import Enum, auto
import sys

class Expression:
    pass

class ExpressionStatement(Expression):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression

class InfixExpression(Expression):
    def __init__(self, lhs: Expression, operation: Token, rhs: Expression):
        self.lhs = lhs
        self.operation = operation
        self.rhs = rhs


class Identifier(Expression):
    def __init__(self, token: Token, value: str, parser: Parser, read_only: bool=False):
        self.token = token
        self.value = value
        self.parser = parser
        self.read_only = read_only
    
    def get(self):
        return self.value

    def set(self, value):
        if self.read_only:
            # call logical errors once that is complete
            return
        self.value = value

class LetStatement(Expression):
    def __init__(self, identifier: Identifier, value: str, type: Token):
        self.identifier = identifier
        self.value = value
        self.type = type

class ConstStatement(Expression):
    def __init__(self, identifier: Identifier, value: str, type: Token):
        self.identifier = identifier
        self.value = value
        self.type = type

class BlockStatement(Expression):
    def __init__(self, statements: Expression):
        self.statements: List[Expression] = statements

class IfExpression:
    def __init__(
        self,
        condition: Expression,
        consequence: BlockStatement,
        alternative: BlockStatement,
    ) -> None:
        self.token = Token.IF
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f"{type(self).__name__} {self.__dict__}"    

class FunctionStatement:
    def __init__(self, variables: List[Tuple[str, Token]], return_value: Variable, block: BlockStatement):
        self.variables = variables
        self.return_value = return_value
        self.block = block

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token, self.curr_str = self.lexer.next_token()
        self.next_token, self.next_str = self.lexer.next_token()
        self.errors = []
        self.symbols: Dict[str, object] = dict()
        self.prefix_parse_fns: dict[Token, Callable[[], [Expression]]] = dict()
        self.infix_parse_fns: dict[Token, Callable[[Expression], [Expression]]] = dict()

        self._register_prefix_fn(Token.IDENTIFIER, self.parse_identifier)
        self._register_prefix_fn(Token.IF, self.parse_if_expression)
        self._register_prefix_fn(Token.FN, self.parse_function_statement)
        self._register_prefix_fn(Token.LET, self.parse_let_statement)
        self._register_prefix_fn(Token.CONST, self.parse_const_statement)

        self._register_infix_fn(Token.EQUAL, self.parse_infix_expression)
        self._register_infix_fn(Token.NOTEQUAL, self.parse_infix_expression)
        self._register_infix_fn(Token.GREATER, self.parse_infix_expression)
        self._register_infix_fn(Token.GREATEREQUAL, self.parse_infix_expression)
        self._register_infix_fn(Token.LESS, self.parse_infix_expression)
        self._register_infix_fn(Token.LESSEQUAL, self.parse_infix_expression)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def _register_prefix_fn(self, token: Token, fn: Callable[[], [Expression]]) -> None:
        self.prefix_parse_fns[token] = fn

    def _register_infix_fn(
        self, token: Token, fn: Callable[[Expression], [Expression]]
    ) -> None:
        self.infix_parse_fns[token] = fn

    def _next_token(self) -> None:
        self.curr_token = self.next_token
        self.curr_str = self.next_str
        self.next_token, self.next_str = self.lexer.next_token()

    def _peek_token_is(self, token: Token) -> bool:
        return self.next_token == token

    def run(self) -> None:
        while self.curr_token != Token.EOF:
            match self.curr_token:
                case Token.IF:
                    print(self.parse_if_expression())
                case _:
                    self.parse_expression_statement()
            self._next_token()

    def parse_function_statement(self) -> FunctionStatement:
        self._next_token()
        identifier: Identifier = self.parse_identifier()
        self._accept_token(Token.LParen)
        identifiers: List[Identifier] = []
        while self.next_token == Token.IDENTIFIER:
            identifier: Identifier = self.parse_identifier
            identifiers.append(identifier)
        self._accept_token(Token.RParen)
        block = self.parse_block_statement()
        fn: FunctionStatement = FunctionStatement(identifiers, None,block)
        return fn

    def parse_let_statement(self) -> LetStatement:
        self._accept_token(Token.LET)
        identifier: Identifier = self.parse_identifier()
        self._accept_token(Token.ASSIGN)
        self.parse_infix_expression()
    
    def parse_const_statement(self) -> ConstStatement:
        pass

    def parse_expression_statement(self) -> ExpressionStatement:
        token, str_repr = self.curr_token, self.curr_str
        expression = self.parse_expression()
        if self._peek_token_is(Token.SEMICOLON):
            self.next_token()
        return ExpressionStatement(token, expression)

    def parse_expression(self) -> Expression | None:
        prefix_parse_fn = self.prefix_parse_fns[self.curr_token]
        if prefix_parse_fn is None:
            return None
        left_exp: Expression = prefix_parse_fn()
        return left_exp

    def parse_infix_expression(self, lhs: Expression) -> InfixExpression | None:
        token, str_repr = self.curr_token, self.curr_str
        self._next_token()
        rhs = self.parse_expression()
        if rhs is None:
            return None
        return InfixExpression(lhs, token, rhs)

    def parse_identifier(self) -> Identifier:
        return Identifier(self.curr_token, self.curr_str)

    def parse_if_expression(self) -> IfExpression | None:
        self._next_token()
        condition = self.parse_expression()
        if self.next_token != Token.LPAREN:
            return None
        consequence = self.parse_block_statement()
        if self.next_token == Token.ELSE:
            alternative = self.parse_block_statement()
        return IfExpression(condition, consequence, alternative)

    def parse_block_statement(self) -> BlockStatement | None:
        self._accept_token(Token.LBRACKETS)
        statements: List[Expression] = []
        while self.curr_token != Token.RBRACKETS:
            statement: Expression = self.parse_expression_statement()
            statements.append(statement)
        self._accept_token(Token.RBRACKETS)
        block: BlockStatement = BlockStatement(statements)
        return block

    def _call_syntax_error(self, expected_tokens: list[str], actual_token: str) -> None:
        message: str = f"SYNTAX ERROR: expected tokens: "
        message += "".join([token + " " for token in expected_tokens])
        message += (
            "\n" + f"actual_token: {actual_token} at line: {self.lex.line_number}"
        )
        sys.exit(message)

    def _accept_token(self, token: Token):
        if self.current_token != token:
            self.call_syntax_error([], self.current_token)
        self._next_token()
