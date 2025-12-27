import unittest

from src import Lexer
from src.tokens import Token


class TestCharString(unittest.TestCase):
    """
    This class performs whitebox testing technique, loop testing on the
    `_read_char_string` method of the `Lexer`. This corresponds to user story
    number: #40 <https://github.com/JackyLeicester/Coursework/issues/40>

    There is only one input to this method that we can control i.e. the input
    string while instantiating the `Lexer` class.

    A same class but under `condition_testing` tests the `if` branches and
    hence this class testing doesn't have 100% coverage for the same.
    """

    # Test 1: while self.ch != start_quote and self.ch != "\0"
    # Case 1: Zero iteration
    def test11(self):
        lexer = Lexer('"')
        (token, _str_repr) = lexer._read_char_string()
        self.assertEqual(token, Token.EOF)

    # Test 1: while self.ch != start_quote and self.ch != "\0"
    # Case 2: One iteration
    def test12(self):
        lexer = Lexer("'a'")
        (token, str_repr) = lexer._read_char_string()
        self.assertEqual(token, Token.CHAR)
        self.assertEqual(str_repr, "a")

    # Test 1: while self.ch != start_quote and self.ch != "\0"
    # Case 3: Many iteration
    def test13(self):
        lexer = Lexer('"this is some string"')
        (token, str_repr) = lexer._read_char_string()
        self.assertEqual(token, Token.STRING)
        self.assertEqual(str_repr, "this is some string")


if __name__ == "__main__":
    unittest.main()
