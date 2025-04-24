import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import tempfile
import json
import os
import webbrowser

from src.intercode.interCodeGenerator import interCodeGenerator
from src.utils.files import Files as FileLoader
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

        # Elegir archivo usando interfaz gráfica
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo .txt de entrada",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        
        if not file_path:
            print("⚠️ No se seleccionó ningún archivo.")
            return

        if not file_path.endswith(".txt"):
            messagebox.showerror("Archivo inválido", "Por favor, selecciona un archivo con extensión .txt.")
            return

        archivo = FileLoader(file_path)
        self.content, lines = archivo.read_file()

        if self.content:
            self.lexic_errors = Errors(self.content)
            self.sintatic_errors = Errors(self.content)
            self.semantic_errors = Errors(self.content)
            
            # Generar código intermedio
            inter_code_generator=interCodeGenerator()
            self.lexer = Lexer(self.lexic_errors)
            self.semantic = Semantic(self.symbol_table, self.semantic_errors, self.lexer,inter_code_generator)
            self.parser = Parser(self.lexer, self.sintatic_errors, self.semantic)

            self.thread = threading.Thread(target=self.run_analysis)
            self.thread.start()

    def run_analysis(self):
        try:
            # Limpiar historial anterior
            path = os.path.join(tempfile.gettempdir(), "tabla_simbolos_iteracion_historial.json")
            if os.path.exists(path):
                os.remove(path)

            tokens = self.lexer.tokenize(self.content)
            self.parser.parse(self.content)
            inter_code_html = "<br>".join(self.semantic.intercode_generator.get_code())

            with open("./templates/compilador.html", "r", encoding="utf-8") as tpl_file:
                template = tpl_file.read()

            html = template.replace("{{LEXICAL_ERRORS}}", self.lexic_errors.errorHtml('lexicos')) \
                           .replace("{{SYNTAX_ERRORS}}", self.sintatic_errors.errorHtml('sintacticos')) \
                           .replace("{{SYMBOL_TABLE}}", self.symbol_table.toHtml()) \
                           .replace("{{TOKENS}}", self.tokens.toHtml(tokens)) \
                           .replace("{{INTER_CODE}}", inter_code_html) 

            # Historial WHILE
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    historial = json.load(f)

                historial_html = '<h2>🌀 Cambios durante los ciclos</h2>'
                for entry in historial:
                    historial_html += f"<h4>Iteración #{entry['iteration']} – {entry['timestamp']}</h4>"
                    historial_html += "<table border='1'><tr><th>Variable</th><th>Valor</th></tr>"
                    for k, v in entry["tabla"].items():
                        historial_html += f"<tr><td>{k}</td><td>{v}</td></tr>"
                    historial_html += "</table><br>"
            else:
                historial_html = "<p>No se registraron cambios durante la ejecución del WHILE.</p>"

            html = html.replace("{{WHILE_HISTORY}}", historial_html)

            with open("./templates/salida.html", "w", encoding="utf-8") as output_file:
                output_file.write(html)

            ruta_absoluta = os.path.abspath("./templates/salida.html")
            webbrowser.open(f"file://{ruta_absoluta}")

        except Exception as e:
            print(" Error en análisis:", e)

if __name__ == "__main__":
    Main()
