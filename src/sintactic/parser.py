import ply.yacc as yacc

class Parser:
    def __init__(self, lexer, sintatic_errors, symbol_table):
        self.lexer = lexer
        self.errors = sintatic_errors
        self.tokens = lexer.tokens
        self.symbol_table = symbol_table
        self.parser = yacc.yacc(module=self, debug=True)

    def p_program(self, p):
        '''program : statement
                   | program statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_declaration(self, p):
        '''declaration : INT IDENTIFIER SEMICOLON
                       | INT IDENTIFIER EQUALS expression SEMICOLON'''
        if len(p) == 4:
            self.symbol_table.add_symbol(p[2], p[1])
            print(f"Declaración de variable: {p[2]}")
        else:
            self.symbol_table.add_symbol(p[2], p[1], p[4])
            print(f"Declaración e inicialización de {p[2]} con valor {p[4]}")
        p[0] = None

    def p_assignment(self, p):
        'assignment : IDENTIFIER EQUALS expression SEMICOLON'
        if self.symbol_table.exists(p[1]):
            self.symbol_table.update_symbol(p[1], p[3])
            print("Asignación:", p[1], "=", p[3])
        else:
            self.errors.encolar_error(f"Error: Variable '{p[1]}' no declarada.")
        p[0] = None

    def p_expression(self, p):
        '''expression : expression PLUS term
                      | expression MINUS term
                      | term'''
        if len(p) == 4:
            val1 = self.symbol_table.get_symbol(p[1]) if isinstance(p[1], str) else p[1]
            val3 = self.symbol_table.get_symbol(p[3]) if isinstance(p[3], str) else p[3]

            if val1 is None or val3 is None:
                self.errors.encolar_error(f"Error: Operación inválida: {p[1]} {p[2]} {p[3]}")
                p[0] = None
            else:
                reserved_inverted = {v: k for k, v in self.lexer.reserved.items()}
                if p[2] == reserved_inverted.get('PLUS'):
                    p[0] = val1 + val3
                elif p[2] == reserved_inverted.get('MINUS'):
                    p[0] = val1 - val3
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
                self.errors.encolar_error("Error: Variable no inicializada")
                p[0] = None
            else:
                reserved_inverted = {v: k for k, v in self.lexer.reserved.items()}
                if p[2] == reserved_inverted.get('TIMES'):
                    p[0] = val1 * val3
                elif p[2] == reserved_inverted.get('DIVIDE'):
                    if val3 != 0:
                        p[0] = val1 / val3
                    else:
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
                self.errors.encolar_error(f"Error: Variable '{p[1]}' no inicializada.")
            p[0] = value
        else:
            p[0] = p[1]

    def p_condition(self, p):
        'condition : expression RELOP expression'
        left_value = p[1]  # El lado izquierdo de la expresión
        operator = p[2]  # El operador relacional
        right_value = p[3]  # El lado derecho de la expresión

        # Evaluar las variables de la condición si son nombres de variables
        if isinstance(left_value, str):
            left_value = self.symbol_table.get_symbol(left_value)
        if isinstance(right_value, str):
            right_value = self.symbol_table.get_symbol(right_value)

        # Comprobamos si alguna de las variables no está inicializada
        if left_value is None or right_value is None:
            self.errors.encolar_error(f"Error: Operación inválida: {left_value} {operator} {right_value}")
            p[0] = False  # En caso de error, la condición será false
        else:
            # Realizamos la comparación según el operador relacional
            if operator == '>':
                p[0] = left_value > right_value
            elif operator == '<':
                p[0] = left_value < right_value
            elif operator == '==':
                p[0] = left_value == right_value
            else:
                self.errors.encolar_error(f"Operador relacional desconocido: {operator}")
                p[0] = False  # En caso de error, la condición será false

    def p_while_loop(self, p):
        'while_loop : WHILE LPAREN condition RPAREN LBRACE program RBRACE'
        print('Reconocido WHILE')

        body = p[6]  # Cuerpo del while
        condition = p[3]  # La condición original (expresión completa)

        while True:
            # Evaluar la condición antes de cada iteración
            condition_value = self.evaluate_condition(condition)

            if not condition_value:  # Si la condición es falsa, salir del ciclo
                break

            print("Ejecutando cuerpo del WHILE")
            for stmt in body:
                if stmt:  # Ejecutar solo si no es None
                    self.parser.parse(stmt, lexer=self.lexer.lexer)

            print("x =", self.symbol_table.get_symbol("x"))  #debug

        p[0] = None

    def evaluate_condition(self, condition):
        """Evalúa la condición de manera flexible."""
        try:
            # Aseguramos que la condición sea una lista con tres elementos
            if not isinstance(condition, list) or len(condition) != 3:
                self.errors.encolar_error("Error: La condición debe ser una lista con tres elementos.")
                return False
            
            # Desempaquetamos los valores
            left_value = condition[0]  # parte izquierda de la condición
            operator = condition[1]  # operador relacional
            right_value = condition[2]  # parte derecha de la condición

            # Evaluar las variables de la condición si son nombres de variables
            if isinstance(left_value, str):
                left_value = self.symbol_table.get_symbol(left_value)
            if isinstance(right_value, str):
                right_value = self.symbol_table.get_symbol(right_value)

            # Comprobamos si alguna de las variables no está inicializada
            if left_value is None or right_value is None:
                self.errors.encolar_error(f"Error: Operación inválida: {left_value} {operator} {right_value}")
                return False

            # Realizamos la comparación según el operador relacional
            if operator == '>':
                return left_value > right_value
            elif operator == '<':
                return left_value < right_value
            elif operator == '==':
                return left_value == right_value
            else:
                self.errors.encolar_error(f"Operador relacional desconocido: {operator}")
                return False
        except Exception as e:
            self.errors.encolar_error(f"Error al evaluar la condición: {e}")
            return False

    def p_statement(self, p):
        '''statement : declaration
                     | assignment
                     | while_loop
                     | expression SEMICOLON'''
        p[0] = p[1]

    def p_error(self, p):
        if p:
            token=self.lexer.get_current_token()
            columna=self.errors.find_column(token)
            fila=self.errors.find_line(token)
            self.errors.encolar_error(f"Error de sintaxis en '{p.value}' en la fila {fila} y columna {columna}")
        else:
            self.errors.encolar_error("Error de sintaxis: expresión incompleta.")

    def parse(self, data):
        self.lexer.lexer.input(data)
        return self.parser.parse(data, lexer=self.lexer.lexer)
