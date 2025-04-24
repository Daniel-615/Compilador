class Semantic:
    def __init__(self, symbol_table, errors, lexer):
        self.symbol_table = symbol_table
        self.errors = errors
        self.lexer = lexer

    def handle_declaration(self, name, var_type, scope, value=None):
        def action():
            self.symbol_table.add_symbol(name, var_type, scope, value)
            if value is not None:
                print(f"Declaración e inicialización de {name} con valor {value}")
            else:
                print(f"Declaración de variable: {name}")
        return action

    def handle_assignment(self, name, value):
        def action():
            # Evalúa la expresión o el valor asignado
            value_eval = self._get_value(value) if not isinstance(value, tuple) else self.handle_expression(*value)
            if self.symbol_table.get_symbol(name) is not None:
                # Actualiza el valor en la tabla de símbolos
                self.symbol_table.update_symbol(name, value_eval)
                print(f"Asignación: {name} = {value_eval}")
            else:
                self.errors.encolar_error(f"Error: Variable '{name}' no declarada.")
        return action

    def handle_expression(self, left, operator, right):
        val1 = self._get_value(left)  # Obtiene el valor del lado izquierdo
        val2 = self._get_value(right)  # Obtiene el valor del lado derecho
        if val1 is None or val2 is None:
            self.errors.encolar_error(f"Error: Operación inválida: {left} {operator} {right}")
            return None
        result = self._apply_operator(val1, operator, val2)  # Aplica el operador
        print(f"Evaluando expresión: {val1} {operator} {val2} = {result}")
        return result

    def handle_term(self, left, operator, right):
        return self.handle_expression(left, operator, right)

    def handle_factor(self, value):
        if isinstance(value, str):  # Si es un identificador
            val = self.symbol_table.get_symbol(value)
            if val is None:
                self.errors.encolar_error(f"Error: Variable '{value}' no inicializada.")
            return val
        return value  # Si es un valor literal, simplemente lo devuelve

    def _get_value(self, item):
        if isinstance(item, str):  # Si es un identificador
            value = self.symbol_table.get_symbol(item)
            if value is None:
                self.errors.encolar_error(f"Error: Variable '{item}' no inicializada.")
            return value
        print(f"Valor literal: {item}")
        return item  # Si es un número literal, simplemente lo devuelve

    def _apply_operator(self, a, op, b):
        # Mapeo de operadores personalizados
        if op == 'cristiano':  # Suma
            return a + b
        if op == 'tchouameni':  # Resta
            return a - b
        if op == 'messi':  # Multiplicación
            return a * b
        if op == 'pepe':  # División
            if b == 0:
                self.errors.encolar_error("Error: División por cero")
                return None
            return a / b
        self.errors.encolar_error(f"Error: Operador no soportado: {op}")
        return None

    def evaluate_condition_dynamic(self, left, op, right):
        val1 = self._get_value(left)  # Obtiene el valor actualizado de la variable izquierda
        val2 = self._get_value(right)  # Obtiene el valor de la constante o variable derecha

        if val1 is None or val2 is None:
            self.errors.encolar_error(f"Error: Condición inválida: {left} {op} {right}")
            return False

        print(f"Evaluando condición: {val1} {op} {val2}")
        if op == '>': return val1 > val2
        if op == '<': return val1 < val2
        if op == '==': return val1 == val2
        self.errors.encolar_error(f"Error: Operador relacional desconocido: {op}")
        return False

    def handle_while(self, condition_fn, body):
        def action():
            print("Reconocido WHILE")
            while condition_fn():  # Evalúa la condición en cada iteración
                print("Evaluando condición del WHILE...")
                for stmt in body:
                    if stmt and callable(stmt):
                        stmt()  # Ejecuta cada sentencia en el cuerpo del while
                print("Estado actual de las variables:", self.symbol_table.symbols)
        return action

    def evaluate_condition(self, condition):
        if not isinstance(condition, list) or len(condition) != 3:
            self.errors.encolar_error("Error: La condición debe tener tres elementos.")
            return False

        left = self._get_value(condition[0])
        op = condition[1]
        right = self._get_value(condition[2])

        if left is None or right is None:
            self.errors.encolar_error(f"Error: Condición inválida: {left} {op} {right}")
            return False

        if op == '>': return left > right
        if op == '<': return left < right
        if op == '==': return left == right
        self.errors.encolar_error(f"Error: Operador relacional desconocido: {op}")
        return False