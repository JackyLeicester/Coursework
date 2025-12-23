from src.lexer import Lexer
import unittest


class ConstantDeclarationTest(unittest.TestCase):
    def test1(self):
        lexer: Lexer = Lexer("A C")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "A")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "C")

    def test2(self):
        lexer: Lexer = Lexer("A    C")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "A")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "C")

    def test3(self):
        lexer: Lexer = Lexer("A\nC")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "A")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "C")

    def test4(self):
        lexer: Lexer = Lexer("A D")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "A")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "D")

    def test5(self):
        lexer: Lexer = Lexer("A    D")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "A")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "D")

    def test6(self):
        lexer: Lexer = Lexer("A\nD")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "A")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "D")

    def test7(self):
        lexer: Lexer = Lexer("B C")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "B")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "C")

    def test8(self):
        lexer: Lexer = Lexer("B    C")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "B")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "C")

    def test9(self):
        lexer: Lexer = Lexer("B\nC")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "B")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "C")

    def test10(self):
        lexer: Lexer = Lexer("B D")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "B")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "D")

    def test11(self):
        lexer: Lexer = Lexer("B    D")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "B")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "D")

    def test12(self):
        lexer: Lexer = Lexer("B\nD")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "B")
        _, str_repr = lexer.next_token()
        self.assertEqual(str_repr, "D")

if __name__ == "__main__":
    unittest.main()