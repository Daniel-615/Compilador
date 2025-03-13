class Token:
    def __init__(self):
        """Inicializa la clase Token con el diccionario de palabras clave y operadores."""
        
        # Lista de todos los posibles tipos de tokens
        self.types = [
            'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
            'EQUALS', 'SEMICOLON', 'LBRACE', 'RBRACE', 'LPAREN', 
            'RPAREN', 'GT', 'LT', 'DOT', 'COMMA', 'QUOTE', 'PRINT', 
            'VOID', 'FUNCTION', 'STRUCT', 'SWITCH'
        ]
        
        # Palabras clave específicas del lenguaje
        self.keywords = {
            # Ciclos
            'Forlan': 'FOR',
            'Walker': 'WHILE',
            'Son': 'DO_WHILE',
            # Condiciones
            'Ronaldinho': 'IF',
            'Zidane': 'ELSE',
            # Retorno
            'Benzema': 'RETURN',
            # Tipos de datos
            'Milito': 'INT',
            'Riquelme': 'FLOAT',
            'Saviola': 'CHAR',
            # Comentarios
            'Maguire': 'COMMENT_SINGLE',
            "Pique y Puyol": 'COMMENT_MULTI',
            # Operadores definidos por palabras
            'Cristiano': 'PLUS',
            'Messi': 'TIMES',
            'Pepe': 'DIVIDE',
            'Tchouaméni': 'MINUS',
            'Casillas': 'PAREN',
            # Mostrar en pantalla
            'Vinicius': 'PRINT',
            # Funciones y estructuras
            'Hazard': 'VOID',
            'Muller': 'FUNCTION',
            'Cavani': 'STRUCT',
            'Suarez': 'SWITCH'
        }

    def get_token(self, palabra):
        """Devuelve el token correspondiente a una palabra clave o lo clasifica como IDENTIFIER."""
        return self.keywords.get(palabra, 'IDENTIFIER')

