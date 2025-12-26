import unittest
from unittest.mock import patch
import io

from src import Lexer, Parser, evaluate
from src.parser import IfExpression, BooleanLiteral, BlockStatement
from src.tokens import Token


class TestIfStatement(unittest.TestCase):
    """
    NOTE: Since there are no loops in the method involved in executing
    `if` statement, there is nothing to test via loop testing and hence
    this class is empty.

    This class performs condition testing on the following:
    - `if` and `else` branch in `_read_identifier` of the `Lexer`.
    - `parse_if_expression` method of `Parser`.
    - Evaluating of "if" statements in `evaluator`

    This corresponds to user story number: #26
    <https://github.com/JackyLeicester/Coursework/issues/26>

    There is only one input that we can control i.e. the input string while
    instantiating the `Lexer` class.
    """

    pass


if __name__ == "__main__":
    unittest.main()
