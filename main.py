from src.utils.files import Files as f
from src.lexer.lexer import Lexer
from src.sintactic.parser import Parser
from src.utils.errors import Errors
from src.semantic.symbolTable import SymbolTable
from src.utils.tokens import Tokens

class Main:
    def __init__(self):
        """
        Inicializa el compilador.
        """
        self.lexic_errors = Errors()  # Errores léxicos -> Graficarlos HTML
        self.sintatic_errors = Errors()  # Errores sintácticos -> Graficarlos HTML
        self.symbol_table = SymbolTable()  # Tabla de símbolos
        self.tokens=Tokens() #Graficar tokens devueltos por el lexer
        file = f("lenguaje.txt")
        content, lines = file.read_file()

        if content:
            try:
                self.lexer = Lexer(self.lexic_errors)
                self.parser = Parser(self.lexer, self.sintatic_errors,self.symbol_table)  
                
                tokens = self.lexer.tokenize(content)

                # Iniciar análisis sintáctico
                self.parser.parse(content)
                
                #Luego cambiar esto por botones en la interfaz
                self.sintatic_errors.errorHtml('Sintácticos')
                self.lexic_errors.errorHtml('Léxicos')
                self.symbol_table.toHtml()
                self.tokens.toHtml(tokens)

            except Exception as e:
                print("Error: ", e)
        else:
            print("No se pudo leer el archivo.")

if __name__ == "__main__":
    Main()