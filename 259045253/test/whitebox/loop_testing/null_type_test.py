import unittest


class TestNullLiteral(unittest.TestCase):
    """
    NOTE: Since there are no loops in the method involved in executing `print`
    statement, there is nothing to test via loop testing and hence this class
    is empty.

    This class performs condition testing on the following:
    - `null` branch in `_read_identifier` of the `Lexer`.
    - `parse_null` method of `Parser`.
    - Evaluating of "null" statements in `evaluator`

    This corresponds to user story number: #109
    <https://github.com/JackyLeicester/Coursework/issues/109>

    There is only one input that we can control i.e. the input string while
    instantiating the `Lexer` class.
    """

    pass


if __name__ == "__main__":
    unittest.main()
