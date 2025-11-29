from enum import Enum, auto


class Token(Enum):
    EOF = auto()
    LET = auto()
    IDENTIFIER = auto()
    SEMICOLON = auto()
    EQUALS = auto()
