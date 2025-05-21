import ply.yacc as yacc

class Parser:
    def __init__(self, lexer, sintatic_errors, semantic_handler):
        self.lexer = lexer
        self.errors = sintatic_errors
        self.semantic = semantic_handler
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)

    precedence = (
        ('left', 'CRISTIANO', 'TCHOUAMENI'),
        ('left', 'MESSI', 'PEPE'),
    )

    def p_program(self, p):
        '''program : statement
                | program statement'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            list1 = p[1] if isinstance(p[1], list) else []
            list2 = [p[2]] if p[2] is not None else []
            p[0] = list1 + list2

    def p_program_empty(self, p):
        'program : '
        p[0] = []

    def p_statement(self, p):
        '''statement : method_declaration
                    | declaration
                    | assignment
                    | while_loop
                    | do_while_loop
                    | for_loop
                    | if_statement
                    | method_call SEMICOLON
                    | expression SEMICOLON
                    | break_statement
                    | COUTINHO LPAREN expression RPAREN SEMICOLON'''

        if p.slice[1].type == 'COUTINHO':
            p[0] = self.semantic.handle_print(p[3])
        else:
            p[0] = p[1] if p[1] is not None else (lambda: None)

    def p_for_init(self, p):
        '''for_init : declaration_no_semicolon
                    | assignment_no_semicolon'''
        p[0] = p[1]

    def p_assignment_no_semicolon(self, p):
        'assignment_no_semicolon : IDENTIFIER EQUALS expression'
        p[0] = self.semantic.handle_assignment(p[1], p[3])

    def p_declaration_no_semicolon(self, p):
        '''declaration_no_semicolon : MILITO IDENTIFIER EQUALS expression
                                    | ZIDANE IDENTIFIER EQUALS expression
                                    | SAVIOLA IDENTIFIER EQUALS expression
                                    | INIESTA IDENTIFIER EQUALS expression
                                    | VALDERRAMA IDENTIFIER EQUALS expression'''
        scope = 'global' if not self.semantic.symbol_table.scope_stack else 'local'
        identifier = p[2]
        value = p[4]
        type_ = p[1]
        p[0] = self.semantic.handle_declaration(identifier, type_, scope, value)

    def p_for_loop(self, p):
        'for_loop : RAMOS LPAREN for_init SEMICOLON condition SEMICOLON assignment_no_semicolon RPAREN LBRACE program RBRACE'
        init = p[3]
        condition = p[5]
        update = p[7]
        body = p[10] if isinstance(p[10], list) else []

        if not callable(condition):
            self.errors.encolar_error(" La condición del for no es válida.")
            p[0] = lambda: None
            return

        p[0] = self.semantic.handle_for(init, condition, update, body)


    def p_do_while_loop(self, p):
        'do_while_loop : AGUERO LBRACE program RBRACE WALKER LPAREN condition RPAREN SEMICOLON'
        body = p[3] if isinstance(p[3], list) else []
        condition = p[7]

        if not callable(condition):
            self.errors.encolar_error(" La condición del do-while no es válida.")
            p[0] = lambda: None
            return

        p[0] = self.semantic.handle_do_while(condition, body)


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
        scope = 'global' if not self.semantic.symbol_table.scope_stack else 'local'
        identifier = p[2]
        value = p[4] if len(p) > 4 else None
        type_ = p[1]
        p[0] = self.semantic.handle_declaration(identifier, type_, scope, value)

    def p_factor_grouped(self, p):
        'factor : LPAREN expression RPAREN'
        if isinstance(p[2], tuple) and len(p[2]) == 3:
            p[0] = self.semantic.handle_expression(*p[2])
        else:
            p[0] = p[2]

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
                | CHAR_LITERAL'''
        print(f" Factor detectado: {p[1]}")
        p[0] = self.semantic.handle_factor(p[1])

    def p_factor_method_call(self, p):
        'factor : method_call'
        p[0] = p[1]  # esto es una función callable, no se debe pasar por handle_factor

    def p_if_statement(self, p):
        '''if_statement : BALLACK LPAREN condition RPAREN LBRACE program RBRACE
                        | BALLACK LPAREN condition RPAREN LBRACE program RBRACE ROBBEN LBRACE program RBRACE'''
        condition = p[3]
        if_body = p[6]
        else_body = p[10] if len(p) > 8 else []

        def scoped_if():
            self.semantic.symbol_table.enter_scope()
            action = self.semantic.handle_if(condition, if_body, else_body)
            action()
            self.semantic.symbol_table.exit_scope()

        p[0] = scoped_if

    def p_condition(self, p):
        'condition : IDENTIFIER RELOP expression'
        print(f" Condición construida: {p[1]} {p[2]} {p[3]}")
        p[0] = self.semantic.evaluate_condition_dynamic(p[1], p[2], p[3])

    def p_while_loop(self, p):
        'while_loop : WALKER LPAREN condition RPAREN LBRACE program RBRACE'
        body = p[6] if isinstance(p[6], list) else []

        if not callable(p[3]):
            self.errors.encolar_error("La condición del while no es válida.")
            p[0] = lambda: None
            return

        # Ya no usamos scoped_while, devolvemos directamente la acción
        p[0] = self.semantic.handle_while(p[3], body)


    def p_method_declaration(self, p):
        'method_declaration : IDENTIFIER LPAREN RPAREN LBRACE program RBRACE'

        method_name = p[1]
        method_body = p[5]

        def define():
            print(f"✅ Definiendo método '{method_name}' (tipo: {type(method_name)})")
            print(f"🔍 Body del método (tipo: {type(method_body)}): {method_body}")
            self.semantic.handle_method_declaration(method_name, method_body)()

        p[0] = define

    def p_method_call(self, p):
        'method_call : IDENTIFIER LPAREN RPAREN'

        method_name = p[1]
        if not isinstance(method_name, str):
            self.errors.encolar_error(f"Error: nombre de método inválido: {method_name} (tipo: {type(method_name)})")
            p[0] = lambda: None
            return

        def call_with_scope():
            self.semantic.symbol_table.enter_scope()
            action = self.semantic.handle_method_call(method_name)
            action()
            self.semantic.symbol_table.exit_scope()

        p[0] = call_with_scope


    def p_switch_statement(self, p):
        'statement : FORLAN LPAREN IDENTIFIER RPAREN LBRACE cases default_case RBRACE'
        print(f"Valor recibido para var_name en switch: {p[3]} | tipo: {type(p[3])}")
        p[0] = self.semantic.handle_switch(p[3], p[6], p[7])

    def p_empty(self, p):
        'empty :'
        p[0] = []

    def p_cases(self, p):
        '''cases : case
                | cases case'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_case(self, p):
        'case : SON value COLON program'
        body = p[4] if isinstance(p[4], list) else [p[4]]
        p[0] = (p[2], body)

    def p_default_case(self, p):
        '''default_case : RONALDINHO COLON program
                        | empty'''
        if len(p) > 2:
            p[0] = p[3] if isinstance(p[3], list) else [p[3]]
        else:
            p[0] = []

    def p_value(self, p):
        '''value : NUMBER
                 | STRING_LITERAL
                 | CHAR_LITERAL'''
        p[0] = p[1]

    def p_break_statement(self, p):
        'break_statement : ROMAN SEMICOLON'
        p[0] = self.semantic.handle_break()
    def p_error(self, p):
        if p:
            try:
                col = self.errors.find_column(p)
                row = self.errors.find_line(p)
                token = p.value.lower() if isinstance(p.value, str) else str(p.value)

                # Errores comunes relacionados con estructuras de control y delimitadores
                if token in {'}', 'walker', 'ballack', 'robben', 'ramos', 'forlan', 'aguero', 'son', 'ronaldinho'}:
                    self.errors.encolar_error(
                        f"Error de sintaxis antes de '{p.value}' en la fila {row} y columna {col}. "
                        f"¿Falta un ';' al final de la instrucción anterior o el bloque anterior no está cerrado?"
                    )

                elif token == '}':
                    self.errors.encolar_error(
                        f"Error de sintaxis en '}}' en la fila {row} y columna {col}. "
                        f"¿Se cerró un bloque sin haberse abierto correctamente?"
                    )
                elif token == '{':
                    self.errors.encolar_error(
                        f"Error de sintaxis en '{{' en la fila {row} y columna {col}. "
                        f"¿Está mal ubicado el inicio del bloque?"
                    )
                elif token == '(':
                    self.errors.encolar_error(
                        f"Error de sintaxis en '(' en la fila {row} y columna {col}. "
                        f"¿Está cerrando correctamente con ')'?"
                        )
                elif token == ')':
                    self.errors.encolar_error(
                        f"Error de sintaxis en ')' en la fila {row} y columna {col}. "
                        f"¿Se abrió correctamente con '('?"
                    )
                elif token == 'robben':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'robben' en la fila {row} y columna {col}. "
                        f"¿El bloque 'if' anterior está cerrado correctamente con '}}'?"
                    )
                elif token == 'walker':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'walker' en la fila {row} y columna {col}. "
                        f"¿Falta el bloque '{{}}' que contiene el cuerpo del ciclo?"
                    )
                elif token == 'ballack':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'ballack' en la fila {row} y columna {col}. "
                        f"¿Falta el bloque '{{}}' que contiene el cuerpo del if?"
                    )

                # Errores comunes semánticos o de estilo
                elif token == 'coutinho':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'coutinho' en la fila {row} y columna {col}. "
                        f"¿Falta el paréntesis con la expresión a imprimir o el punto y coma final?"
                    )
                elif token.startswith('"') or token.startswith("'"):
                    self.errors.encolar_error(
                        f"Error: literal mal cerrado en la fila {row} y columna {col}."
                    )
                elif token.isdigit() and not p.type == 'NUMBER':
                    self.errors.encolar_error(
                        f"Error: identificador no válido '{p.value}' en la fila {row} y columna {col}. "
                        f"Los identificadores no pueden comenzar con números."
                    )
                elif token in {'cristiano', 'tchouameni', 'messi', 'pepe'}:
                    self.errors.encolar_error(
                        f"Error de sintaxis: operador '{token}' usado incorrectamente o sin operandos en la fila {row} y columna {col}."
                    )
                elif token in {'milito', 'zidane', 'saviola', 'iniesta', 'valderrama'}:
                    self.errors.encolar_error(
                        f"Error: falta identificador después del tipo '{token}' en la fila {row} y columna {col}."
                    )
                elif token.isidentifier():
                    self.errors.encolar_error(
                        f"Error de sintaxis en '{p.value}' en la fila {row} y columna {col}. "
                        f"¿Falta un ';' al final de la instrucción?"
                    )
                elif token.isidentifier():
                    self.errors.encolar_error(
                        f"Error de sintaxis antes de '{p.value}' en la fila {row} y columna {col}. "
                        f"¿Falta un ';' al final de la instrucción anterior o el bloque anterior no está cerrado?"
                    )
                else:
                    self.errors.encolar_error(
                        f"Error de sintaxis en '{p.value}' en la fila {row} y columna {col}."
                    )

            except Exception:
                self.errors.encolar_error("Error de sintaxis en token inesperado.")

        else:
            # Fin del archivo: probablemente falta una llave de cierre
            self.errors.encolar_error(
                "Error de sintaxis: expresión incompleta o final inesperado. ¿Falta cerrar una llave '}' de alguna estructura?"
            )




    def parse(self, data):
        self.lexer.lexer.input(data)
        parsed = self.parser.parse(data, lexer=self.lexer.lexer)
        print(" Parsing completado. Ejecutando AST...")
        self.semantic.symbol_table.enter_scope()
        if parsed:
            for stmt in parsed:
                print(f"STMT Desde el parser:{stmt}")
                if callable(stmt):
                    stmt()
        self.semantic.symbol_table.guardar_snapshot_final()
        self.semantic.symbol_table.toHtml()
        self.semantic.symbol_table.exit_scope()
        return parsed