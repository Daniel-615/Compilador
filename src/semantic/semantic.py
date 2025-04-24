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
            evaluated_value = value if isinstance(value, (int, float, bool, str)) else self._get_value(value)
            self.symbol_table.add_symbol(name, var_type, scope, evaluated_value)
            print(f"🟢 Declaración: {name} = {evaluated_value}")
        return action

    def handle_assignment(self, name, value):
        def action():
            self._wait_if_paused()
            print(f"📦 Recibido en asignación para '{name}': {value}")
            try:
                value_eval = None
                if isinstance(value, tuple):
                    if len(value) == 3:
                        value_eval = self.handle_expression(*value)
                    else:
                        self.errors.encolar_error(f"❌ Error: La expresión para '{name}' debe tener 3 elementos (left, op, right), pero tiene {len(value)}.")
                        print(f"❌ Tupla inválida para '{name}': {value}")
                        return
                else:
                    value_eval = self._get_value(value)

                if self.symbol_table.get_symbol(name) is not None:
                    self.symbol_table.update_symbol(name, value_eval)
                    print(f"🔁 Asignación: {name} = {value_eval}")
                else:
                    self.errors.encolar_error(f"❌ Error: Variable '{name}' no declarada.")
            except Exception as e:
                self.errors.encolar_error(f"❌ Error al asignar a '{name}': {e}")
                print(f"❌ Error al asignar a '{name}': {e}")
        return action




    def handle_expression(self, left, operator, right):
        self._wait_if_paused()
        val1 = self._get_value(left)
        val2 = self._get_value(right)
        if val1 is None or val2 is None:
            self.errors.encolar_error(f"❌ Error: Operación inválida: {left} {operator} {right}")
            return None
        result = self._apply_operator(val1, operator, val2)
        print(f"🧠 Evaluación: {val1} {operator} {val2} = {result}")
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
        try:
            if op == 'cristiano':
                return a + b if type(a) == type(b) else self._op_error(op, a, b)
            if op == 'tchouameni':
                return a - b if self._check_numeric(a, b) else self._op_error(op, a, b)
            if op == 'messi':
                return a * b if self._check_numeric(a, b) else self._op_error(op, a, b)
            if op == 'pepe':
                if b == 0:
                    self.errors.encolar_error("❌ Error: División por cero.")
                    return None
                return a / b if self._check_numeric(a, b) else self._op_error(op, a, b)
        except Exception as e:
            self.errors.encolar_error(f"❌ Error en operación: {e}")
        self.errors.encolar_error(f"❌ Operador no válido: {op}")
        return None

    def _check_numeric(self, a, b):
        return isinstance(a, (int, float)) and isinstance(b, (int, float))

    def _op_error(self, op, a, b):
        self.errors.encolar_error(f"❌ No se puede aplicar '{op}' entre {type(a).__name__} y {type(b).__name__}")
        return None

    def evaluate_condition_dynamic(self, left, op, right):
        def safe_get(val):
            return self.symbol_table.get_symbol(val) if isinstance(val, str) and val in self.symbol_table.symbols else val

        def condition():
            val1 = safe_get(left)
            val2 = safe_get(right)
            try:
                result = eval(f"{val1} {op} {val2}")
                print(f"🔍 Evaluando condición: {val1} {op} {val2} → {result}")
                return result
            except Exception as e:
                self.errors.encolar_error(f"❌ Condición inválida: {left} {op} {right} → {e}")
                return False

        return condition

    def handle_while(self, condition_fn, body):
        def action():
            print(f"🔄 WHILE detectado, cuerpo recibido: {body}")
            iteration = 0
            try:
                print(condition_fn.__name__)
                while condition_fn():
                    self._wait_if_paused()
                    iteration += 1
                    print(f"🔁 Iteración #{iteration} del WHILE")
                    print(f"[DEBUG] Tipo de body: {type(body)}")
                    for i, stmt in enumerate(body):
                        try:
                            if callable(stmt):
                                print(f"  ▶ Ejecutando instrucción #{i+1} del cuerpo...")
                                stmt()
                            else:
                                print(f"  ⚠ Instrucción #{i+1} no es callable: {stmt}")
                        except Exception as inner_err:
                            self.errors.encolar_error(f"❌ Error al ejecutar instrucción #{i+1} del WHILE: {inner_err}")
                            print(f"❌ Error en instrucción #{i+1}: {inner_err}")
                    self._save_iteration_state()
            except Exception as e:
                self.errors.encolar_error(f"❌ Error general en el cuerpo del WHILE: {e}")
                print(f"❌ Error general en el cuerpo del WHILE: {e}")
        return action







    def handle_method_declaration(self, name, body):
        def action():
            self._wait_if_paused()
            self.methods[name] = body
            print(f"📌 Método '{name}' definido.")
        return action

    def handle_method_call(self, name):
        def action():
            self._wait_if_paused()
            if name in self.methods:
                print(f"📞 Llamando a método '{name}'...")
                for stmt in self.methods[name]:
                    if callable(stmt):
                        stmt()
            else:
                self.errors.encolar_error(f"❌ Error: Método '{name}' no está definido.")
        return action
    def _save_iteration_state(self):
        import json, os, tempfile
        from datetime import datetime
        temp_dir = tempfile.gettempdir()
        path = os.path.join(temp_dir, "tabla_simbolos_iteracion.json")
        estado = {
            "timestamp": datetime.now().isoformat(),
            "tabla": self.symbol_table.symbols
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=4)
