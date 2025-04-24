import ply.lex as lex

class Lexer:
    tokens = [
        'NUMBER', 'IDENTIFIER', 'EQUALS', 'SEMICOLON', 'LBRACE', 'RBRACE',
        'LPAREN', 'RPAREN', 'GT', 'LT', 'DOT', 'COMMA', 'QUOTE',
        'RELOP', 'STRING_LITERAL', 'CHAR_LITERAL','COLON',
    ]

    reserved = {
        'messi': 'MESSI',# *
        'pepe': 'PEPE',# /
        'tchouameni': 'TCHOUAMENI', # -
        'ronaldinho': 'RONALDINHO', #default
        'cristiano': 'CRISTIANO', # +
        'robben': 'ROBBEN', #else
        'milito': 'MILITO', #int
        'zidane': 'ZIDANE',  # float
        'saviola': 'SAVIOLA',  # char
        'iniesta': 'INIESTA',  # string
        'valderrama': 'VALDERRAMA',  # boolean
        'walker': 'WALKER', #while
        'son': 'SON', #case
        'forlan': 'FORLAN', #Switch
        'global': 'GLOBAL',
        'local': 'LOCAL',
        'ballack': 'BALLACK', #if
        'coutinho': 'COUTINHO', #mostrar
        'aguero': 'AGUERO', #do
        
    }

    tokens += list(reserved.values())
    t_COLON = r':'

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
    t_QUOTE = r'"'

    t_ignore = ' \t'

    def __init__(self, errors):
        self.errors = errors
        self.lexer = lex.lex(module=self)
    def t_COMMENT_SINGLELINE(self, t):
        r'\/\/.*'
        pass  # Ignora comentarios de línea

    def t_COMMENT_MULTILINE(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        pass  # Ignora comentarios multilínea

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_STRING_LITERAL(self, t):
        r'"([^\\"]|\\.)*"'
        t.value = t.value[1:-1]
        return t

    def t_CHAR_LITERAL(self, t):
        r'\'(.*?)\''
        t.value = t.value[1:-1]
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

    def set_error(self, error, position):
        token = self.get_current_token()
        columna = self.errors.find_column(token)
        fila = self.errors.find_line(token)
        self.errors.encolar_error(f"Error léxico: '{error}' en la fila {fila} y columna {columna} ")

    def tokenize(self, data):
        self.lexer.input(data)
        tokens = [(tok.type, tok.value) for tok in self.lexer]
        return tokens
