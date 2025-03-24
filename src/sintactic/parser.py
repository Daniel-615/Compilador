import ply.yacc as yacc

class Parser:
    def __init__(self, lexer, sintatic_errors,symbol_table):
        """Inicializa el parser con el lexer"""
        self.lexer = lexer
        self.errors = sintatic_errors
        self.tokens = lexer.tokens  
        self.symbol_table = symbol_table
        self.parser = yacc.yacc(module=self, debug=True) 

    def p_program(self, p):
        '''program : statement
                   | program statement'''
        print("Reconocido programa")

    # Declaraciones de variables (Ejemplo: milito x;)
    def p_declaration(self, p):
        '''declaration : INT IDENTIFIER SEMICOLON
                    | INT IDENTIFIER EQUALS expression SEMICOLON'''
        if len(p) == 4:
            self.symbol_table.add_symbol(p[2], p[1])
            print(f"Declaración de variable: {p[2]}")
        else:
            self.symbol_table.add_symbol(p[2], p[1], p[4])
            print(f"Declaración e inicialización de {p[2]} con valor {p[4]}")


    #Asignaciones (Ejemplo: x = 10;)
    def p_assignment(self, p):
        'assignment : IDENTIFIER EQUALS expression SEMICOLON'
        if self.symbol_table.exists(p[1]):
            self.symbol_table.update_symbol(p[1], p[3])
            print("Asignación:", p[1], "=", p[3])
        else:
            print(f"Error: Variable '{p[1]}' no declarada.")
            self.errors.encolar_error(f"Error: Variable '{p[1]}' no declarada.")

    # (Ejemplo: x cristiano 1)
    def p_expression(self, p):
        '''expression : expression PLUS term
                    | expression MINUS term
                    | term'''
        if len(p) == 4:
            val1 = self.symbol_table.get_symbol(p[1]) if isinstance(p[1], str) else p[1]
            val3 = self.symbol_table.get_symbol(p[3]) if isinstance(p[3], str) else p[3]
            
            if val1 is None or val3 is None:
                print(f"Error: No se pueden operar identificadores sin valores definidos. {p[1]} {p[2]} {p[3]}")
                self.errors.encolar_error(f"Error: Operación inválida entre identificadores y números: {p[1]} {p[2]} {p[3]}")
                p[0] = None
            else:
                reserved_inverted = {v: k for k, v in self.lexer.reserved.items()} # Invertir clave por valor
                if p[2]==reserved_inverted.get('PLUS'):
                    p[0] = val1 + val3
                elif p[2]==reserved_inverted.get('MINUS'):
                    p[0]=val1-val3
                else:
                    self.errors.encolar_error(f"Error: Operador '{p[2]}' no reconocido.")
                    p[0] = None 
        else:
            p[0] = p[1]

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | factor'''
        if len(p) == 4:
            val1 = self.symbol_table.get_symbol(p[1]) if isinstance(p[1], str) else p[1]
            val3 = self.symbol_table.get_symbol(p[3]) if isinstance(p[3], str) else p[3]
            
            if val1 is None or val3 is None:
                print("Error: Operación con variable no inicializada")
                self.errors.encolar_error("Error: Operación con variable no inicializada")
                p[0] = None
            else:
                reserved_inverted = {v: k for k, v in self.lexer.reserved.items()} # Invertir clave por valor
                if p[2] == reserved_inverted.get('TIMES'):
                    p[0] = val1 * val3
                elif p[2] == reserved_inverted.get('DIVIDE') and val3 != 0:
                    p[0] = val1 / val3
                else:
                    print("Error: División por cero")
                    self.errors.encolar_error("Error: División por cero")
                    p[0] = None
        else:
            p[0] = p[1]

    def p_factor(self, p):
        '''factor : NUMBER
                  | IDENTIFIER'''
        if isinstance(p[1], str):
            value = self.symbol_table.get_symbol(p[1])
            if value is None:
                print(f"Error: Variable '{p[1]}' no inicializada.")
                self.errors.encolar_error(f"Error: Variable '{p[1]}' no inicializada.")
            p[0] = value
        else:
            p[0] = p[1]

    # Condiciones (Ejemplo: x > 5)
    def p_condition(self, p):
        'condition : expression RELOP expression'

    

    def p_while_loop(self, p):
        'while_loop : WHILE LPAREN condition RPAREN LBRACE program RBRACE'
        print("Inicio de bucle WHILE")

    # Instrucciones generales (statement)
    def p_statement(self, p):
        '''statement : declaration
                    | assignment
                    | while_loop
                    | expression SEMICOLON'''
        print("Reconocido statement")

    # Manejo de errores sintácticos
    def p_error(self, p):
        if p:
            error_message = f"Error de sintaxis en '{p.value}' en la posición {p.lexpos}"
        else:
            error_message = "Error de sintaxis en la entrada (expresión incompleta)."
        self.errors.encolar_error(error_message)
        print(error_message)

    # Método para iniciar el parser
    def parse(self, data):
        print("\n=== Tokens Generados ===")
        self.lexer.lexer.input(data)
        for tok in self.lexer.lexer:
            print(tok)
        print("========================\n")
        
        return self.parser.parse(data, lexer=self.lexer.lexer)