import ply.lex as lex
from src.lexer.tokens import Token 

class Lexer:
    def __init__(self,errors):
        self.token_obj = Token()
        self.errors=errors 
        self.tokens = list(self.token_obj.keywords.values()) + [  
            'NUMBER', 'IDENTIFIER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
            'SEMICOLON', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'GT', 'LT', 
            'DOT', 'COMMA', 'QUOTE'
        ]  
        self.lexer = lex.lex(module=self)  
    def set_error(self, error, position):
        error_message = f"Error léxico: '{error}' en la posición {position}"
        self.errors.encolar_error(error_message)

    # Reglas para operadores y símbolos especiales
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_TIMES     = r'\*'
    t_DIVIDE    = r'/'
    t_EQUALS    = r'='
    t_SEMICOLON = r';'
    t_LBRACE    = r'\{'
    t_RBRACE    = r'\}'
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_GT        = r'>'
    t_LT        = r'<'
    t_DOT       = r'\.'
    t_COMMA     = r','
    t_QUOTE     = r'\"'

    # Regla para palabras clave e identificadores
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.token_obj.get_token(t.value)  # Si es palabra clave, usa su token; si no, es IDENTIFIER
        return t

    # Regla para números
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)  # Convierte a entero
        return t

    # Ignorar espacios y tabulaciones
    t_ignore = " \t"

    # Manejo de errores léxicos
    def t_error(self, t):
        self.set_error(t.value[0], t.lexpos)
        t.lexer.skip(1)  # Avanza el lexer para evitar bucles infinitos

    # Método para analizar un texto
    def tokenize(self, data):
        self.lexer.input(data)
        return [(tok.type, tok.value) for tok in self.lexer]

