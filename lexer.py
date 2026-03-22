# lexer.py

from tokens import *

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        # assumes current_char is '/' and next is '*'
        self.advance()  # skip /
        self.advance()  # skip *

        while self.current_char is not None:
            if self.current_char == '*' and self.peek() == '/':
                self.advance()  # skip *
                self.advance()  # skip /
                return
            self.advance()

        raise Exception("Lexical Error: unclosed comment")

    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.text):
            return self.text[next_pos]
        return None

    def identifier(self):
        result = ""
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        if result == "safe":
            return Token(SAFE, result)
        elif result == "sah":
            return Token(SAH, result)
        elif result == "ebas":
            return Token(EBAS, result)
        else:
            return Token(IDENTIFIER, result)

    def number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(NUMBER, int(result))

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() == '*':
                self.skip_comment()
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, "=")

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, "-")

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, "*")

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, "/")

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ";")

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ")")

            raise Exception(f"Lexical Error: invalid character '{self.current_char}'")

        return Token(EOF, None)

    def tokenize(self):
        tokens = []
        token = self.get_next_token()

        while token.type != EOF:
            tokens.append(token)
            token = self.get_next_token()

        tokens.append(token)  # add EOF
        return tokens