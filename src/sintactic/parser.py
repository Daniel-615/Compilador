import ply.yacc as yacc
from src.semantic.symbolTable import SymbolTable

class Parser:
    def __init__(self, lexer, sintatic_errors):
        """Inicializa el parser con el lexer"""
        self.lexer = lexer
        self.errors = sintatic_errors
        self.tokens=lexer.tokens
        self.symbol_table = SymbolTable()
        self.parser = yacc.yacc(module=self)
        
    #Reconocimiento de variables int, float, char
    def p_declaration(self, p):
        '''declaration : INT IDENTIFIER SEMICOLON
                       | FLOAT IDENTIFIER SEMICOLON
                       | CHAR IDENTIFIER SEMICOLON'''
        self.symbol_table.add_symbol(p[2], p[1])  

    # Regla para asignaciones (x = 10;)
    def p_assignment(self, p):
        'assignment : IDENTIFIER EQUALS expression SEMICOLON'
        self.symbol_table.update_symbol(p[1], p[3])  

    # Expresiones matemáticas
    def p_expression_plus(self, p):
        "expression : expression PLUS term"
        p[0] = p[1] + p[3]

    def p_expression_term(self, p):
        "expression : term"
        p[0] = p[1]

    def p_term_times(self, p):
        "term : term TIMES factor"
        p[0] = p[1] * p[3]

    def p_term_factor(self, p):
        "term : factor"
        p[0] = p[1]

    def p_factor_number(self, p):
        "factor : NUMBER"
        p[0] = p[1]

    def p_error(self, p):
        if p:
            error_message = f"Error de sintaxis en '{p.value}' en la posición {p.lexpos}"
            self.errors.encolar_error(error_message)
            print(error_message)
        else:
            error_message = "Error de sintaxis en la entrada (expresión incompleta)."
            self.errors.encolar_error(error_message)
            print(error_message)

    def p_program(self, p):
        '''program : declaration
                   | assignment
                   | expression
                   | program declaration
                   | program assignment
                   | program expression'''

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)
