# PARSER FINAL Y SEMANTIC CORREGIDO CON FUNCIONES Y MÉTODOS
import ply.yacc as yacc

class Parser:
    def __init__(self, lexer, sintatic_errors, semantic_handler):
        self.lexer = lexer
        self.errors = sintatic_errors
        self.semantic = semantic_handler
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, debug=True)

    def p_program(self, p):
        '''program : statement
                   | program statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        '''statement : declaration
                     | assignment
                     | while_loop
                     | method_declaration
                     | method_call SEMICOLON
                     | expression SEMICOLON'''
        p[0] = p[1]

    def p_declaration(self, p):
        '''declaration : MILITO IDENTIFIER SEMICOLON
                       | MILITO IDENTIFIER EQUALS expression SEMICOLON
                       | ZIDANE IDENTIFIER SEMICOLON
                       | ZIDANE IDENTIFIER EQUALS expression SEMICOLON
                       | SAVIOLA IDENTIFIER SEMICOLON
                       | SAVIOLA IDENTIFIER EQUALS expression SEMICOLON
                       | INIESTA IDENTIFIER SEMICOLON
                       | INIESTA IDENTIFIER EQUALS expression SEMICOLON
                       | VALDERRAMA IDENTIFIER SEMICOLON
                       | VALDERRAMA IDENTIFIER EQUALS expression SEMICOLON'''
        scope = 'local'
        identifier = p[2]
        value = p[4] if len(p) > 4 else None
        type_ = p[1]
        p[0] = self.semantic.handle_declaration(identifier, type_, scope, value)

    def p_assignment(self, p):
        'assignment : IDENTIFIER EQUALS expression SEMICOLON'
        p[0] = self.semantic.handle_assignment(p[1], p[3])

    def p_expression(self, p):
        '''expression : expression CRISTIANO term
                      | expression TCHOUAMENI term
                      | term'''
        if len(p) == 4:
            p[0] = (p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_term(self, p):
        '''term : term MESSI factor
                | term PEPE factor
                | factor'''
        if len(p) == 4:
            p[0] = (p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_factor(self, p):
        '''factor : NUMBER
                  | IDENTIFIER
                  | STRING_LITERAL
                  | CHAR_LITERAL
                  | method_call'''
        p[0] = self.semantic.handle_factor(p[1])

    def p_condition(self, p):
        'condition : IDENTIFIER RELOP expression'
        p[0] = lambda: self.semantic.evaluate_condition_dynamic(p[1], p[2], p[3])

    def p_while_loop(self, p):
        'while_loop : WALKER LPAREN condition RPAREN LBRACE program RBRACE'
        p[0] = self.semantic.handle_while(p[3], p[6])

    def p_method_declaration(self, p):
        'method_declaration : IDENTIFIER LPAREN RPAREN LBRACE program RBRACE'
        p[0] = self.semantic.handle_method_declaration(p[1], p[5])

    def p_method_call(self, p):
        'method_call : IDENTIFIER LPAREN RPAREN'
        p[0] = self.semantic.handle_method_call(p[1])

    def p_error(self, p):
        if p:
            token = self.lexer.get_current_token()
            col = self.errors.find_column(token)
            row = self.errors.find_line(token)
            self.errors.encolar_error(f"Error de sintaxis en '{p.value}' en la fila {row} y columna {col}")
        else:
            self.errors.encolar_error("Error de sintaxis: expresión incompleta.")

    def parse(self, data):
        self.lexer.lexer.input(data)
        parsed = self.parser.parse(data, lexer=self.lexer.lexer)
        if parsed:
            for stmt in parsed:
                if callable(stmt):
                    stmt()
        return parsed