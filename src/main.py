from argparse import ArgumentParser, RawDescriptionHelpFormatter
from lexer import Lexer
from parser import Parser
import textwrap


def read_file_contents(filename: str) -> str | None:
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
    arg_parser.add_argument("file", help=": program read from script file")
    arg_parser.add_argument("--debug", action="store_true", help="enable debug output")
    args = arg_parser.parse_args()

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

    # Reset lexer for parsing
    lexer = Lexer(contents)
    parser = Parser(lexer)
    if args.debug:
        print("=== PARSING ===")
    parser.run()


if __name__ == "__main__":
    main()
