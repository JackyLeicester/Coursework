from argparse import ArgumentParser, RawDescriptionHelpFormatter
from .lexer import Lexer
from .parser import Parser
from .evaluator import evaluate
import textwrap
import code


class Repl(code.InteractiveConsole):
    env = {}

    def runsource(self, source: str, filename="<input>", symbol="single"):
        lexer = Lexer(source)
        parser = Parser(lexer)
        expressions = parser.run()
        evaluate(expressions, self.env)


def read_file_contents(filename: str) -> str | None:
    if filename is None:
        raise ValueError("filename cannot be None")
    try:
        with open(filename, "r") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print(f"error: file `{filename}` doesn't exist")
        return None


def main():
    arg_parser = ArgumentParser(
        prog="interpret",
        description=textwrap.dedent("""
        An interpreter for simple programming language developed for Software Measurement and
        Quality Assurance coursework.

        Checkout https://github.com/JackyLeicester/Coursework for the syntax of the language.
        """),
        formatter_class=RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Copyright © 2025
        Jacky Liang Xu, Myrza Danike, Syed Fasiuddin, Vatsal Chaudhari."""),
    )
    arg_parser.add_argument("file", nargs="?", help=": program read from script file")
    arg_parser.add_argument("--debug", action="store_true", help="enable debug output")

    args = arg_parser.parse_args()

    if not args.file:
        repl = Repl()
        repl.interact(banner="", exitmsg="")
        exit(0)

    contents = read_file_contents(args.file)
    if not contents:
        exit(1)

    lexer = Lexer(contents)

    # Debug: Will execute if run with "--debug" argument
    if args.debug:
        print("=== TOKENS ===")
        token, token_str = lexer.next_token()
        while token.name != "EOF":
            print(f"{token.name:15} {token_str}")
            token, token_str = lexer.next_token()
        print(f"{token.name:15} {token_str}")

    lexer = Lexer(contents)
    parser = Parser(lexer)
    expressions = parser.run()
    evaluate(expressions)
