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
                     | expression SEMICOLON'''
        p[0] = p[1]

    def p_declaration(self, p):
        '''declaration : INT IDENTIFIER SEMICOLON
                       | INT IDENTIFIER EQUALS expression SEMICOLON'''
        if len(p) == 4:
            p[0] = self.semantic.handle_declaration(p[2], p[1])
        else:
            p[0] = self.semantic.handle_declaration(p[2], p[1], p[4])

    def p_assignment(self, p):
        'assignment : IDENTIFIER EQUALS expression SEMICOLON'
        p[0] = self.semantic.handle_assignment(p[1], p[3])

    def p_expression(self, p):
        '''expression : expression PLUS term
                      | expression MINUS term
                      | term'''
        if len(p) == 4:
            p[0] = self.semantic.handle_expression(p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | factor'''
        if len(p) == 4:
            p[0] = self.semantic.handle_term(p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_factor(self, p):
        '''factor : NUMBER
                  | IDENTIFIER'''
        p[0] = self.semantic.handle_factor(p[1])

    def p_condition(self, p):
        'condition : IDENTIFIER RELOP expression'
        # Pasamos el nombre (string) y la expresión evaluable
        var_name = p[1]  # Esto es un string como 'x'
        op = p[2]
        value_expr = p[3]
        p[0] = lambda: self.semantic.evaluate_condition_dynamic(var_name, op, value_expr)



    def p_while_loop(self, p):
        'while_loop : WHILE LPAREN condition RPAREN LBRACE program RBRACE'
        p[0] = self.semantic.handle_while(p[3], p[6])

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
        parsed= self.parser.parse(data, lexer=self.lexer.lexer)
        if parsed:  # Ejecutamos el programa principal
            for stmt in parsed:
                if callable(stmt):
                    stmt()
        
        return parsed
