import threading
import tempfile
import json

import os
import webbrowser
from src.utils.files import Files as f
from src.lexer.lexer import Lexer
from src.sintactic.parser import Parser
from src.utils.errors import Errors
from src.semantic.symbolTable import SymbolTable
from src.semantic.semantic import Semantic
from src.utils.tokens import Tokens

class Main:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.tokens = Tokens()

        file_path = input("Por favor, ingrese la ruta del archivo de entrada: ")
        archivo = f(file_path)
        self.content, lines = archivo.read_file()

        if self.content:
            self.lexic_errors = Errors(self.content)
            self.sintatic_errors = Errors(self.content)
            self.semantic_errors = Errors(self.content)

            self.lexer = Lexer(self.lexic_errors)
            self.semantic = Semantic(self.symbol_table, self.semantic_errors, self.lexer)
            self.parser = Parser(self.lexer, self.sintatic_errors, self.semantic)

            self.thread = threading.Thread(target=self.run_analysis)
            self.thread.start()

    def run_analysis(self):
        try:
            path = os.path.join(tempfile.gettempdir(), "tabla_simbolos_iteracion_historial.json")
            if os.path.exists(path):
                os.remove(path)
            tokens = self.lexer.tokenize(self.content)
            self.parser.parse(self.content)

            # Leer HTML base
            with open("./templates/compilador.html", "r", encoding="utf-8") as tpl_file:
                template = tpl_file.read()

            # Inyectar resultados
            html = template.replace("{{LEXICAL_ERRORS}}", self.lexic_errors.errorHtml('lexicos')) \
                           .replace("{{SYNTAX_ERRORS}}", self.sintatic_errors.errorHtml('sintacticos')) \
                           .replace("{{SYMBOL_TABLE}}", self.symbol_table.toHtml()) \
                           .replace("{{TOKENS}}", self.tokens.toHtml(tokens))
            # Leer historial del while
            with open(os.path.join(tempfile.gettempdir(), "tabla_simbolos_iteracion_historial.json"), "r", encoding="utf-8") as f:
                historial = json.load(f)

            historial_html = '<h2>🌀 Cambios durante el WHILE</h2>'
            for entry in historial:
                historial_html += f"<h4>Iteración #{entry['iteration']} – {entry['timestamp']}</h4>"
                historial_html += "<table border='1'><tr><th>Variable</th><th>Valor</th></tr>"
                for k, v in entry["tabla"].items():
                    historial_html += f"<tr><td>{k}</td><td>{v}</td></tr>"
                historial_html += "</table><br>"

            # Reemplaza o añade una nueva sección en tu HTML
            html = html.replace("{{WHILE_HISTORY}}", historial_html)


            with open("./templates/salida.html", "w", encoding="utf-8") as output_file:
                output_file.write(html)

            ruta_absoluta = os.path.abspath("./templates/salida.html")
            webbrowser.open(f"file://{ruta_absoluta}")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main = Main()

