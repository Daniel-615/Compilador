from src.utils.files import Files as f
from src.lexer.lexer import Lexer
from src.sintactic.parser import Parser
from src.utils.errors import Errors
from src.semantic.symbolTable import SymbolTable
from src.semantic.semantic import Semantic
from src.utils.tokens import Tokens

class Main:
    def __init__(self):
        """
        Inicializa el compilador.
        """
        
        self.symbol_table = SymbolTable()  # Tabla de símbolos
        self.tokens=Tokens() #Graficar tokens devueltos por el lexer
        file = f("lenguaje.txt")
        self.content, lines = file.read_file()

        if self.content:
            try:
                self.lexic_errors = Errors(self.content)  # Errores léxicos -> Graficarlos HTML
                self.sintatic_errors = Errors(self.content)  # Errores sintácticos -> Graficarlos HTML
                self.semantic_errors=Errors(self.content)
                self.lexer = Lexer(self.lexic_errors)
                self.semantic=Semantic(self.symbol_table,self.semantic_errors,self.lexer) 
                self.parser = Parser(self.lexer, self.sintatic_errors, self.semantic)

                
                
                tokens = self.lexer.tokenize(self.content)

                # Iniciar análisis sintáctico
                self.parser.parse(self.content)
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