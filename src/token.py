from enum import Enum, auto


class Token(Enum):
    EOF = auto()
    LET = auto()
    IDENTIFIER = auto()
    LITERAL = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    INT = auto()
    CHAR = auto()
    STRING = auto()
    IF = auto()
    ELSE = auto()
