class Semantic:
    def __init__(self, symbol_table, errors, lexer):
        self.symbol_table = symbol_table
        self.errors = errors
        self.lexer = lexer
        self.methods = {}  # Diccionario para guardar métodos

    def handle_declaration(self, name, var_type, scope, value=None):
        def action():
            if isinstance(value, (int, float, bool)):
                evaluated_value = value
            else:
                evaluated_value = self._get_value(value) if value is not None else None
            self.symbol_table.add_symbol(name, var_type, scope, evaluated_value)
            if evaluated_value is not None:
                print(f"Declaración e inicialización de {name} con valor {evaluated_value}")
            else:
                print(f"Declaración de variable: {name}")
        return action

    def handle_assignment(self, name, value):
        def action():
            if isinstance(value, tuple):
                value_eval = self.handle_expression(*value)
            else:
                value_eval = self._get_value(value)
            if self.symbol_table.get_symbol(name) is not None:
                self.symbol_table.update_symbol(name, value_eval)
                print(f"Asignación: {name} = {value_eval}")
            else:
                self.errors.encolar_error(f"Error: Variable '{name}' no declarada.")
        return action

    def handle_expression(self, left, operator, right):
        val1 = self._get_value(left)
        val2 = self._get_value(right)
        if val1 is None or val2 is None:
            self.errors.encolar_error(f"Error: Operación inválida: {left} {operator} {right}")
            return None
        result = self._apply_operator(val1, operator, val2)
        print(f"Evaluando expresión: {val1} {operator} {val2} = {result}")
        return result

    def handle_term(self, left, operator, right):
        return self.handle_expression(left, operator, right)

    def handle_factor(self, value):
        if isinstance(value, str) and value in self.symbol_table.symbols:
            return self.symbol_table.get_symbol(value)
        return value

    def _get_value(self, item):
        if isinstance(item, str) and item in self.symbol_table.symbols:
            return self.symbol_table.get_symbol(item)
        return item

    def _apply_operator(self, a, op, b):
        if op == 'cristiano':
            if isinstance(a, str) and isinstance(b, str):
                return a + b
            elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return a + b
            else:
                self.errors.encolar_error(f"Error: No se puede sumar {type(a).__name__} con {type(b).__name__}")
                return None
        if op == 'tchouameni':
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return a - b
            else:
                self.errors.encolar_error(f"Error: No se puede restar {type(a).__name__} con {type(b).__name__}")
                return None
        if op == 'messi':
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return a * b
            else:
                self.errors.encolar_error(f"Error: No se puede multiplicar {type(a).__name__} con {type(b).__name__}")
                return None
        if op == 'pepe':
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                if b == 0:
                    self.errors.encolar_error("Error: División por cero")
                    return None
                return a / b
            else:
                self.errors.encolar_error(f"Error: No se puede dividir {type(a).__name__} con {type(b).__name__}")
                return None
        self.errors.encolar_error(f"Error: Operador no soportado: {op}")
        return None

    def evaluate_condition_dynamic(self, left, op, right):
        val1 = self._get_value(left)
        val2 = self._get_value(right)
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
            while condition_fn():
                print("Evaluando condición del WHILE...")
                for stmt in body:
                    if stmt and callable(stmt):
                        stmt()
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

    def handle_method_declaration(self, name, body):
        def action():
            self.methods[name] = body
            print(f"Método '{name}' definido.")
        return action

    def handle_method_call(self, name):
        def action():
            if name in self.methods:
                print(f"Llamando al método '{name}'...")
                for stmt in self.methods[name]:
                    if callable(stmt):
                        stmt()
            else:
                self.errors.encolar_error(f"Error: Método '{name}' no está definido.")
        return action
