from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from interpreter import Interpreter

import io
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json["code"]
    input_values = request.json.get("inputs", [])

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        parser.parse()

        semantic = SemanticAnalyzer(tokens)
        semantic.analyze()

        interpreter = Interpreter(tokens, input_values=input_values)

        old_stdout = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer

        interpreter.interpret()

        sys.stdout = old_stdout
        output = buffer.getvalue()

        return jsonify({
            "status": "success",
            "output": output if output.strip() else "Program executed successfully."
        })

    except Exception as e:
        sys.stdout = sys.__stdout__
        return jsonify({
            "status": "error",
            "output": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)