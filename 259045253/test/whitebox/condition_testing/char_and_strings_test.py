import unittest

from src import Lexer, Parser, evaluate
from src.parser import CharLiteral, StringLiteral
from src.tokens import Token


class TestCharString(unittest.TestCase):
    """
    This class performs condition testing on the following:
    - `_read_char_string` method of the `Lexer`.
    - `parse_char` and `parse_string` method of `Parser`.
    - Evaluating of string and character literals in `evaluator`

    This corresponds to user story number: #40
    <https://github.com/JackyLeicester/Coursework/issues/40>

    There is only one input to this method that we can control i.e. the input
    string while instantiating the `Lexer` class.
    """

    @staticmethod
    def setup_parser(src: str) -> Parser:
        lexer = Lexer(src)
        return Parser(lexer)

    # Test 1: self.ch == "\0"
    def test_lexer1(self):
        lexer = Lexer('"')
        (token, _str_repr) = lexer._read_char_string()
        self.assertEqual(token, Token.EOF)

    # Test 2: word.startswith("'") and word.endswith("'") -> T T
    # Case 1: len(word) == 2 or len(word) == 3 -> T
    def test_lexer21(self):
        lexer = Lexer("'c'")
        (token, str_repr) = lexer._read_char_string()
        self.assertEqual(token, Token.CHAR)
        self.assertEqual(str_repr, "c")

    # Test 2: word.startswith("'") and word.endswith("'") -> T T
    # Case 2: len(word) == 2 or len(word) == 3 -> F
    def test_lexer22(self):
        lexer = Lexer("'foo'")
        (token, _str_repr) = lexer._read_char_string()
        self.assertEqual(token, Token.EOF)

    # Test 3: len(word) >= 2 and word.startswith('"') and word.endswith('"')
    def test_lexer3(self):
        lexer = Lexer('"string"')
        (token, str_repr) = lexer._read_char_string()
        self.assertEqual(token, Token.STRING)
        self.assertEqual(str_repr, "string")

    # Test 4: all conditions fail, falls to last line of function
    def test_lexer4(self):
        lexer = Lexer("aaa")
        self.assertRaises(Exception, lexer._read_char_string)

    # Test 1: `parse_char` method
    def test_parser1(self):
        parser = self.setup_parser("'a'")
        char = parser.parse_char()
        self.assertIsInstance(char, CharLiteral)
        self.assertEqual("a", char.literal)

    # Test 2: `parse_string` method
    def test_parser2(self):
        parser = self.setup_parser('"foo bar"')
        string = parser.parse_string()
        self.assertIsInstance(string, StringLiteral)
        self.assertEqual("foo bar", string.literal)

    # Test 1: `CharLiteral` handling in `_evaluator` function
    def test_evaluator1(self):
        parser = self.setup_parser("'a'")
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(result, "a")

    # Test 2: `CharLiteral` handling in `_evaluator` function
    def test_evaluator2(self):
        parser = self.setup_parser('"foo bar"')
        expressions = parser.run()
        result = evaluate(expressions)
        self.assertEqual(result, "foo bar")


if __name__ == "__main__":
    unittest.main()
