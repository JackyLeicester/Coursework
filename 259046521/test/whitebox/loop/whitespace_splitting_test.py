from src.lexer import Lexer
import unittest


class WhiteSpaceSplitting(unittest.TestCase):
    # loop testing cannot be fully applied to the read_identifier function will never be ran with empty text
    def test1(self):
        lexer = Lexer("a")
        _, word = lexer.next_token()
        self.assertEqual(word, "a")

    def test2(self):
        lexer = Lexer("abc")
        _, word = lexer.next_token()
        self.assertEqual(word, "abc")
