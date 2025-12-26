import unittest


class TestContinueStmt(unittest.TestCase):
    """
    NOTE: Since there are no loops in the method involved in executing
    `continue` statement, there is nothing to test via loop testing and hence
    this class is empty.

    This class performs loop testing on the following:
    - `continue` branch in `_read_identifier` of the `Lexer`.
    - `parse_continue_statement` method of `Parser`.
    - Evaluating of continue statements in `evaluator`

    This corresponds to user story number: #8
    <https://github.com/JackyLeicester/Coursework/issues/8>

    There is only one input that we can control i.e. the input string while
    instantiating the `Lexer` class.
    """

    pass


if __name__ == "__main__":
    unittest.main()
