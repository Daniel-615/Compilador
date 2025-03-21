from src.utils.files import Files as f
from src.lexer.lexer import Lexer
from src.sintactic.parser import Parser
from src.utils.errors import Errors

class Main:
    def __init__(self):
        """
        Inicializa el compilador.
        """
        self.lexic_errors = Errors()  # Errores léxicos -> Graficarlos HTML
        self.sintatic_errors = Errors()  # Errores sintácticos -> Graficarlos HTML

        file = f("lenguaje.txt")
        content, lines = file.read_file()

        if content:
            try:
                self.lexer = Lexer(self.lexic_errors)
                self.parser = Parser(self.lexer, self.sintatic_errors)  
                
                tokens = self.lexer.tokenize(content)
                print("Tokens encontrados:", tokens)

                # Iniciar análisis sintáctico
                self.parser.parse(content)
                self.sintatic_errors.errorHtml('Sintácticos')
                self.lexic_errors.errorHtml('Léxicos')

            except Exception as e:
                print("Error: ", e)
        else:
            print("No se pudo leer el archivo.")

if __name__ == "__main__":
    Main()