from enum import Enum, auto


class Token(Enum):
    EOF = auto()
    LET = auto()
    IDENTIFIER = auto()
    LITERAL = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    STRING = auto()
    EQUAL = auto()
    NOTEQUAL = auto()
    GREATER = auto()
    GREATEREQUAL = auto()
    LESS = auto()
    LESSEQUAL = auto()
