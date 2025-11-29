from enum import Enum, auto

class Token(Enum):
    EOF = auto()
    LET = auto()
    IDENTIFIER = auto()
    # STRING = auto()
    # INTEGER = auto()
    # FLOAT = auto()
    LITERAL = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
