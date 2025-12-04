from enum import IntEnum, auto
from functools import total_ordering


@total_ordering
class Token(IntEnum):
    LOWEST_PRECEDENCE = auto()
    EOF = auto()
    LET = auto()
    CONST = auto()
    IDENTIFIER = auto()
    LITERAL = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    STRING = auto()
    IF = auto()
    ELSE = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKETS = auto()
    RBRACKETS = auto()
    TRUE = auto()
    FALSE = auto()
<<<<<<<< HEAD:src/mytoken.py
    FUNCTION = auto()
========

    OR = auto()
    AND = auto()
    EQUAL = auto()
    NOTEQUAL = auto()
    LESS = auto()
    LESSEQUAL = auto()
    GREATER = auto()
    GREATEREQUAL = auto()

    NOT = auto()
>>>>>>>> 7741bc9bbd96a1521ce16386c95e96b95af07ff3:src/tokens.py
    PLUS = auto()
    MINUS = auto()
    ASTERISK = auto()
    SLASH = auto()
    FOR = auto()
