from argparse import ArgumentParser
from lexer import Lexer
from parser import Parser

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
        prog="smqa-interpreter",
        description="The interpreter for a toy language developed as a coursework for SMQA",
    )
    arg_parser.add_argument("filename")
    args = arg_parser.parse_args()

    contents = read_file_contents(args.filename)
    if not contents:
        exit(1)

    lexer = Lexer(contents)
    parser = Parser(lexer)
    parser.parse_file()

if __name__ == "__main__":
    main()
