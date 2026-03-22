from tokens import *

class Interpreter:
    def __init__(self, tokens, input_values=None):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.variables = {}
        self.input_values = input_values or []
        self.input_index = 0

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            current = self.current_token
            self.advance()
            return current
        else:
            raise Exception(
                f"Runtime Error: expected {token_type}, got {self.current_token.type}"
            )

    def interpret(self):
        while self.current_token.type != EOF:
            self.statement()

    def statement(self):
        if self.current_token.type == SAFE:
            self.declaration()
        elif self.current_token.type == SAH:
            self.input_stmt()
        elif self.current_token.type == EBAS:
            self.output_stmt()
        elif self.current_token.type == IDENTIFIER:
            self.assignment()
        else:
            raise Exception(f"Runtime Error: unexpected token {self.current_token}")

    def declaration(self):
        self.eat(SAFE)
        var_name = self.eat(IDENTIFIER).value
        self.variables[var_name] = 0
        self.eat(SEMICOLON)

    def input_stmt(self):
        self.eat(SAH)
        var_name = self.eat(IDENTIFIER).value

        if self.input_index >= len(self.input_values):
            raise Exception(f"Runtime Error: missing input for '{var_name}'")

        try:
            value = int(self.input_values[self.input_index])
        except ValueError:
            raise Exception(f"Runtime Error: input for '{var_name}' must be an integer")

        self.input_index += 1
        self.variables[var_name] = value
        self.eat(SEMICOLON)

    def output_stmt(self):
        self.eat(EBAS)
        value = self.expression()
        print(value)
        self.eat(SEMICOLON)

    def assignment(self):
        var_name = self.eat(IDENTIFIER).value
        self.eat(ASSIGN)
        value = self.expression()
        self.variables[var_name] = value
        self.eat(SEMICOLON)

    def expression(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            if self.current_token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif self.current_token.type == DIVIDE:
                self.eat(DIVIDE)
                divisor = self.factor()
                if divisor == 0:
                    raise Exception("Runtime Error: division by zero")
                result //= divisor

        return result

    def factor(self):
        if self.current_token.type == NUMBER:
            return self.eat(NUMBER).value
        elif self.current_token.type == IDENTIFIER:
            var_name = self.eat(IDENTIFIER).value
            return self.variables[var_name]
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expression()
            self.eat(RPAREN)
            return result
        else:
            raise Exception(f"Runtime Error: invalid factor {self.current_token}")