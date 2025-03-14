import ply.lex as lex

class Lexer:
    tokens = [
        'NUMBER', 'IDENTIFIER', 'EQUALS', 'SEMICOLON', 'LBRACE', 'RBRACE', 
        'LPAREN', 'RPAREN', 'GT', 'LT', 'DOT', 'COMMA', 'QUOTE', 'PLUS', 
        'MINUS', 'TIMES', 'DIVIDE'
    ]

    # Palabras reservadas
    reserved = {
        'walker': 'IF',
        'else': 'ELSE',
        'int': 'INT',       
        'float': 'FLOAT',   
        'char': 'CHAR'      
    }

    # Agregamos las palabras reservadas a los tokens
    tokens += list(reserved.values())

    # Reglas para los operadores y símbolos especiales
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

    # Ignorar espacios y tabulaciones
    t_ignore = " \t"

    def __init__(self, errors):
        self.errors = errors
        self.lexer = lex.lex(module=self)

    def set_error(self, error, position):
        error_message = f"Error léxico: '{error}' en la posición {position}"
        self.errors.encolar_error(error_message)

    # Regla para identificadores y palabras clave
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        # Verificar si es una palabra reservada
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    # Regla para números
    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    # Contar líneas
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Manejo de errores
    def t_error(self, t):
        self.set_error(t.value[0], t.lexpos)
        t.lexer.skip(1)

    # Método para analizar texto
    def tokenize(self, data):
        self.lexer.input(data)
        return [(tok.type, tok.value) for tok in self.lexer]
