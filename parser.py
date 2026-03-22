# parser.py

from tokens import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(
                f"Syntax Error: expected {token_type}, got {self.current_token.type}"
            )

    def parse(self):
        while self.current_token.type != EOF:
            self.statement()

    # ---- STATEMENTS ----

    def statement(self):
        if self.current_token.type == SAFE:
            self.declaration()
            self.eat(SEMICOLON)

        elif self.current_token.type == SAH:
            self.input_stmt()
            self.eat(SEMICOLON)

        elif self.current_token.type == EBAS:
            self.output_stmt()
            self.eat(SEMICOLON)

        elif self.current_token.type == IDENTIFIER:
            self.assignment()
            self.eat(SEMICOLON)

        else:
            raise Exception(f"Syntax Error: unexpected token {self.current_token}")

    def declaration(self):
        self.eat(SAFE)
        self.eat(IDENTIFIER)

    def input_stmt(self):
        self.eat(SAH)
        self.eat(IDENTIFIER)

    def output_stmt(self):
        self.eat(EBAS)
        self.expression()

    def assignment(self):
        self.eat(IDENTIFIER)
        self.eat(ASSIGN)
        self.expression()

    # ---- EXPRESSIONS ----

    def expression(self):
        self.term()
        while self.current_token.type in (PLUS, MINUS):
            self.advance()
            self.term()

    def term(self):
        self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            self.advance()
            self.factor()

    def factor(self):
        if self.current_token.type == NUMBER:
            self.eat(NUMBER)

        elif self.current_token.type == IDENTIFIER:
            self.eat(IDENTIFIER)

        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            self.expression()
            self.eat(RPAREN)

        else:
            raise Exception(f"Syntax Error: invalid factor {self.current_token}")