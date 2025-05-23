import ply.lex as lex

class Lexer:
    tokens = [
        'NUMBER', 'IDENTIFIER', 'EQUALS', 'SEMICOLON', 'LBRACE', 'RBRACE',
        'LPAREN', 'RPAREN', 'GT', 'LT', 'DOT', 'COMMA', 'QUOTE',
        'RELOP', 'STRING_LITERAL', 'CHAR_LITERAL', 'COLON',
    ]

    reserved = {
        'messi': 'MESSI',
        'pepe': 'PEPE',
        'tchouameni': 'TCHOUAMENI',
        'ronaldinho': 'RONALDINHO',
        'cristiano': 'CRISTIANO',
        'robben': 'ROBBEN',
        'milito': 'MILITO',
        'zidane': 'ZIDANE',
        'saviola': 'SAVIOLA',
        'iniesta': 'INIESTA',
        'valderrama': 'VALDERRAMA',
        'walker': 'WALKER',
        'son': 'SON',
        'forlan': 'FORLAN',
        'global': 'GLOBAL',
        'local': 'LOCAL',
        'ballack': 'BALLACK',
        'coutinho': 'COUTINHO',
        'aguero': 'AGUERO',
        'ramos': 'RAMOS',
        'roman': 'ROMAN',
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
        self.reported_errors = set()
        self.lexer = lex.lex(module=self)

    def get_pos(self, t):
        fila = t.lexer.lexdata[:t.lexpos].count('\n') + 1
        last_newline = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
        columna = t.lexpos + 1 if last_newline < 0 else t.lexpos - last_newline
        return fila, columna

    def encolar_error_unico(self, msg):
        if msg not in self.reported_errors:
            self.reported_errors.add(msg)
            self.errors.encolar_error(msg)

    def t_COMMENT_SINGLELINE(self, t):
        r'\/\/.*'
        pass

    def t_COMMENT_MULTILINE(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        pass

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_STRING_LITERAL_UNCLOSED(self, t):
        r'"([^\\"]|\\.)*$'
        fila, col = self.get_pos(t)
        self.encolar_error_unico(f"Error léxico: cadena de texto no cerrada en la fila {fila} y columna {col}.")
        t.lexer.skip(1)

    def t_STRING_LITERAL(self, t):
        r'"([^\\"]|\\.)*"'
        t.value = t.value[1:-1]
        if t.value.strip() == "":
            fila, col = self.get_pos(t)
            self.encolar_error_unico(f"Advertencia: cadena vacía en fila {fila}, columna {col}.")
        return t

    def t_CHAR_LITERAL_UNCLOSED(self, t):
        r"'([^\\'\n]|\\.)*$"
        fila, col = self.get_pos(t)
        self.encolar_error_unico(f"Error léxico: carácter no cerrado en la fila {fila} y columna {col}.")
        t.lexer.skip(1)

    def t_CHAR_LITERAL(self, t):
        r"'(.*?)'"
        contenido = t.value[1:-1]
        if len(contenido) != 1:
            fila, col = self.get_pos(t)
            self.encolar_error_unico(f"Error léxico: carácter inválido '{t.value}' en fila {fila}, columna {col}.")
            return None
        t.value = contenido
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        fila, col = self.get_pos(t)
        self.encolar_error_unico(f"Error léxico: carácter no reconocido '{t.value[0]}' en la fila {fila} y columna {col}.")
        t.lexer.skip(1)

    def get_current_token(self):
        return self.lexer.token()

    def set_error(self, error, position):
        token = self.get_current_token()
        fila, col = self.get_pos(token)
        self.encolar_error_unico(f"Error léxico: '{error}' en la fila {fila} y columna {col}")

    def tokenize(self, data):
        self.lexer.input(data)
        tokens = [(tok.type, tok.value) for tok in self.lexer]
        return tokens
