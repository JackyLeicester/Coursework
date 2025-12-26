import unittest

from src import Lexer, Parser, evaluate
from src.parser import ForStatement
from src.tokens import Token


class TestForLoop(unittest.TestCase):
    """
    NOTE: Since there are no loops in the method involved in executing
    `for` statement, there is nothing to test via loop testing and hence
    this class is empty.

    This class performs condition testing on the following:
    - `for` branch in `_read_identifier` of the `Lexer`.
    - `parse_for_statement` method of `Parser`.
    - Evaluating of for statements in `evaluator`

    This corresponds to user story number: #8
    <https://github.com/JackyLeicester/Coursework/issues/8>

    There is only one input that we can control i.e. the input string while
    instantiating the `Lexer` class.
    """

    pass


if __name__ == "__main__":
    unittest.main()
