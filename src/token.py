from enum import Enum, auto


class Token(Enum):
    EOF = auto()
    LET = auto()
    IDENTIFIER = auto()
    LITERAL = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    INT = auto()
