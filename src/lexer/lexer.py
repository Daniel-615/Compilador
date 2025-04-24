import ply.lex as lex

class Lexer:
    tokens = [
        'NUMBER', 'IDENTIFIER', 'EQUALS', 'SEMICOLON', 'LBRACE', 'RBRACE', 
        'LPAREN', 'RPAREN', 'GT', 'LT', 'DOT', 'COMMA', 'QUOTE',
        'RELOP'
    ]

    # Palabras reservadas como tokens explícitos (basados en nombres literales del lenguaje fuente)
    reserved = {
        'messi': 'MESSI',
        'pepe': 'PEPE',
        'tchouameni': 'TCHOUAMENI',
        'ronaldinho': 'RONALDINHO',
        'cristiano': 'CRISTIANO',
        'else': 'ELSE',
        'milito': 'MILITO',
        'zidane': 'ZIDANE',
        'saviola': 'SAVIOLA',
        'walker': 'WALKER',
        'son': 'SON',
        'forlan': 'FORLAN',
        'global': 'GLOBAL',  
        'local': 'LOCAL'
    }

    # Agregamos las palabras reservadas como tokens válidos
    tokens += list(reserved.values())

    # Reglas para operadores y símbolos
    t_RELOP = r'==|!=|<|>|<=|>='
    t_CRISTIANO = r'\+'
    t_TCHOUAMENI = r'-'
    t_MESSI = r'\*'
    t_PEPE = r'/'
    t_EQUALS = r'='
    t_SEMICOLON = r';'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_GT = r'>'
    t_LT = r'<'
    t_DOT = r'\.'
    t_COMMA = r','
    t_QUOTE = r'\"'

    # Ignorar espacios y tabs
    t_ignore = " \t"

    def __init__(self, errors):
        self.errors = errors
        self.lexer = lex.lex(module=self)

    def set_error(self, error, position):
        token = self.get_current_token()
        columna = self.errors.find_column(token)
        fila = self.errors.find_line(token)
        error_message = f"Error léxico: '{error}' en la fila {fila} y columna {columna} "
        self.errors.encolar_error(error_message)

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')  # Retorna el token del nombre reservado o IDENTIFIER
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        self.set_error(t.value[0], t.lexpos)
        t.lexer.skip(1)

    def get_current_token(self):
        return self.lexer.token()

    def tokenize(self, data):
        self.lexer.input(data)
        tokens = [(tok.type, tok.value) for tok in self.lexer]
        return tokens
