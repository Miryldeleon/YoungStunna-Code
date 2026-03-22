from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from interpreter import Interpreter

def main():
    try:
        with open("sample.ysc", "r") as file:
            source_code = file.read()

        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        parser.parse()

        semantic = SemanticAnalyzer(tokens)
        semantic.analyze()

        print("=" * 40)
        print("      YoungStunna Code Compiler")
        print("=" * 40)
        print("Syntax Analysis: PASSED")
        print("Semantic Analysis: PASSED")
        print("Symbol Table:", semantic.symbol_table)
        print("-" * 40)
        print("Program Output:")

        interpreter = Interpreter(tokens)
        interpreter.interpret()

        print("=" * 40)
        print("Execution finished successfully.")
        print("=" * 40)

    except Exception as e:
        print("=" * 40)
        print("YoungStunna Code Compiler Error")
        print("=" * 40)
        print(e)
        print("=" * 40)

if __name__ == "__main__":
    main()