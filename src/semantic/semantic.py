# semantic.py
import time
from threading import Event

class Semantic:
    def __init__(self, symbol_table, errors, lexer, pause_event: Event = None):
        self.symbol_table = symbol_table
        self.errors = errors
        self.lexer = lexer
        self.methods = {}
        self.pause_event = pause_event or Event()

    def _wait_if_paused(self):
        while self.pause_event and not self.pause_event.is_set():
            print("\n⏸ Ejecución pausada... Esperando reanudación.")
            time.sleep(0.3)

    def handle_declaration(self, name, var_type, scope, value=None):
        def action():
            self._wait_if_paused()
            if isinstance(value, (int, float, bool)):
                evaluated_value = value
            else:
                evaluated_value = self._get_value(value) if value is not None else None
            self.symbol_table.add_symbol(name, var_type, scope, evaluated_value)
            print(f"Declaración de {name} = {evaluated_value}")
        return action

    def handle_assignment(self, name, value):
        def action():
            self._wait_if_paused()
            value_eval = self.handle_expression(*value) if isinstance(value, tuple) else self._get_value(value)
            if self.symbol_table.get_symbol(name) is not None:
                self.symbol_table.update_symbol(name, value_eval)
                print(f"Asignación: {name} = {value_eval}")
            else:
                self.errors.encolar_error(f"Error: Variable '{name}' no declarada.")
        return action

    def handle_expression(self, left, operator, right):
        self._wait_if_paused()
        val1 = self._get_value(left)
        val2 = self._get_value(right)
        if val1 is None or val2 is None:
            self.errors.encolar_error(f"Error: Operación inválida: {left} {operator} {right}")
            return None
        result = self._apply_operator(val1, operator, val2)
        print(f"Evaluando: {val1} {operator} {val2} = {result}")
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
        if op == 'cristiano': return a + b if type(a) == type(b) else None
        if op == 'tchouameni': return a - b
        if op == 'messi': return a * b
        if op == 'pepe': return a / b if b != 0 else None
        self.errors.encolar_error(f"Operador no válido: {op}")
        return None

    def evaluate_condition_dynamic(self, left, op, right):
        val1 = self._get_value(left)
        val2 = self._get_value(right)
        if val1 is None or val2 is None:
            self.errors.encolar_error(f"Condición inválida: {left} {op} {right}")
            return False
        return eval(f"{val1} {op} {val2}")

    def handle_while(self, condition_fn, body):
        def action():
            print("WHILE detectado")
            while condition_fn():
                self._wait_if_paused()
                for stmt in body:
                    if callable(stmt):
                        stmt()
        return action

    def handle_method_declaration(self, name, body):
        def action():
            self._wait_if_paused()
            self.methods[name] = body
            print(f"Método '{name}' definido.")
        return action

    def handle_method_call(self, name):
        def action():
            self._wait_if_paused()
            if name in self.methods:
                print(f"Llamando a '{name}'...")
                for stmt in self.methods[name]:
                    if callable(stmt):
                        stmt()
            else:
                self.errors.encolar_error(f"Error: Método '{name}' no definido.")
        return action