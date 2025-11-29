import sys

class Parser:
    def __repr__(self):
        return f"{type(self).__name__}()"


    def call_syntax_erorr(self, expected_tokens: list[str], actual_token: str, line_number: int)->None:
        message: str = "SYNTAX ERROR: expected tokens: ".join([token + " " for token in expected_tokens])
        message += "\n" + f"actual_token: {actual_token} at line: {line_number}"
        sys.exit(message)

    def call_runtime_error(self, message: str, line_number: int):
        message: str = f"RUNTIME ERROR: {message} at line: {line_number}"
        sys.exit(message)