from argparse import ArgumentParser, RawDescriptionHelpFormatter
from lexer import Lexer
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
    args = arg_parser.parse_args()

    contents = read_file_contents(args.file)
    if not contents:
        exit(1)

    lexer = Lexer(contents)

if __name__ == "__main__":
    main()
