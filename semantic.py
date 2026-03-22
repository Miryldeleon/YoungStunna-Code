# semantic.py

from tokens import *

class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.symbol_table = {}

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None

    def analyze(self):
        while self.current_token.type != EOF:
            if self.current_token.type == SAFE:
                self.handle_declaration()
            elif self.current_token.type == SAH:
                self.handle_input()
            elif self.current_token.type == EBAS:
                self.advance()
                self.check_expression()
                self.expect_semicolon()
            elif self.current_token.type == IDENTIFIER:
                self.handle_assignment()
            else:
                self.advance()

    def handle_declaration(self):
        self.advance()  # skip SAFE

        if self.current_token.type != IDENTIFIER:
            raise Exception("Semantic Error: expected identifier after 'safe'")

        var_name = self.current_token.value

        if var_name in self.symbol_table:
            raise Exception(f"Semantic Error: variable '{var_name}' already declared")

        self.symbol_table[var_name] = None
        self.advance()

        self.expect_semicolon()

    def handle_input(self):
        self.advance()  # skip SAH

        if self.current_token.type != IDENTIFIER:
            raise Exception("Semantic Error: expected identifier after 'sah'")

        var_name = self.current_token.value

        if var_name not in self.symbol_table:
            raise Exception(f"Semantic Error: variable '{var_name}' not declared")

        self.advance()
        self.expect_semicolon()

    def handle_assignment(self):
        var_name = self.current_token.value

        if var_name not in self.symbol_table:
            raise Exception(f"Semantic Error: variable '{var_name}' not declared")

        self.advance()  # skip identifier

        if self.current_token.type != ASSIGN:
            raise Exception("Semantic Error: expected '=' in assignment")

        self.advance()  # skip '='
        self.check_expression()
        self.expect_semicolon()

    def check_expression(self):
        while self.current_token.type not in (SEMICOLON, EOF):
            if self.current_token.type == IDENTIFIER:
                var_name = self.current_token.value
                if var_name not in self.symbol_table:
                    raise Exception(f"Semantic Error: variable '{var_name}' not declared")
            self.advance()

    def expect_semicolon(self):
        if self.current_token.type == SEMICOLON:
            self.advance()
        else:
            raise Exception("Semantic Error: missing semicolon")