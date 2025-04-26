import json, os, tempfile
from datetime import datetime

class Semantic:
    def __init__(self, symbol_table, errors, lexer, intercode_generator):
        self.symbol_table = symbol_table
        self.errors = errors
        self.lexer = lexer
        self.methods = {}
        self.intercode_generator = intercode_generator

    def handle_declaration(self, name, var_type, scope, value=None):
        def action():
            evaluated_value = value if isinstance(value, (int, float, bool, str)) else self._get_value(value)
            self.symbol_table.add_symbol(name, var_type, scope, evaluated_value)
            print(f"Declaración: {name} = {evaluated_value}")
        return action

    def handle_assignment(self, name, value):
        def action():
            print(f"Recibido en asignación para '{name}': {value}")
            try:
                if isinstance(value, tuple) and len(value) == 3:
                    value_eval = self.handle_expression(*value)
                else:
                    value_eval = self._get_value(value)

                if self.symbol_table.get_symbol(name) is not None:
                    self.symbol_table.update_symbol(name, value_eval)
                    print(f"Asignación: {name} = {value_eval}")
                    self.intercode_generator.emit(f"{name} = {value_eval}")
                else:
                    self.errors.encolar_error(f" Error: Variable '{name}' no declarada.")
            except Exception as e:
                self.errors.encolar_error(f" Error al asignar a '{name}': {e}")
        return action

    def _map_operator(self, op):
        return {
            'cristiano': '+',
            'tchouameni': '-',
            'messi': '*',
            'pepe': '/'
        }.get(op, op)

    def handle_expression(self, left, operator, right):
        val1 = self._get_value(left)
        val2 = self._get_value(right)

        if val1 is None or val2 is None:
            self.errors.encolar_error(f" Error: Operación inválida: {left} {operator} {right}")
            return None

        temp = self.intercode_generator.new_temp()
        self.intercode_generator.emit(f"{temp} = {val1} {self._map_operator(operator)} {val2}")
        return temp

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

    def evaluate_condition_dynamic(self, left, op, right):
        left_val = self._get_value(left)
        right_val = self._get_value(right)

        temp = self.intercode_generator.new_temp()
        self.intercode_generator.emit(f"{temp} = {left_val} {op} {right_val}")

        def condition():
            try:
                result = eval(f"{left_val} {op} {right_val}")
                print(f" Evaluando condición: {left_val} {op} {right_val} → {result}")
                return result
            except Exception as e:
                self.errors.encolar_error(f" Condición inválida: {left_val} {op} {right_val} → {e}")
                return False

        return temp, condition

    def handle_while(self, condition_data, body):
        def action():
            print(f" WHILE detectado, cuerpo recibido: {body}")
            label_start = self.intercode_generator.new_label()
            label_end = self.intercode_generator.new_label()

            self.intercode_generator.emit(f"{label_start}:")

            cond_temp, real_condition = condition_data
            self.intercode_generator.emit(f"ifFalse {cond_temp} goto {label_end}")

            while real_condition():
                for stmt in body:
                    if callable(stmt):
                        stmt()

                cond_temp, real_condition = self.evaluate_condition_dynamic(cond_temp, ">", 0)
                self.intercode_generator.emit(f"ifFalse {cond_temp} goto {label_end}")

            self.intercode_generator.emit(f"goto {label_start}")
            self.intercode_generator.emit(f"{label_end}:")
        return action

    def handle_do_while(self, condition_fn, body):
        def action():
            label_start = self.intercode_generator.new_label()
            self.intercode_generator.emit(f"{label_start}:")
            while True:
                for stmt in body:
                    if callable(stmt):
                        stmt()
                if not condition_fn():
                    break
            self.intercode_generator.emit(f"goto {label_start}")
        return action

    def handle_for(self, init_stmt, condition_data, update_stmt, body):
        def action():
            print(" Iniciando ciclo FOR")
            init_stmt()

            label_start = self.intercode_generator.new_label()
            label_end = self.intercode_generator.new_label()

            self.intercode_generator.emit(f"{label_start}:")

            cond_temp, real_condition = condition_data
            self.intercode_generator.emit(f"ifFalse {cond_temp} goto {label_end}")

            while real_condition():
                for stmt in body:
                    if callable(stmt):
                        stmt()
                update_stmt()
                cond_temp, real_condition = self.evaluate_condition_dynamic(cond_temp, ">", 0)
                self.intercode_generator.emit(f"goto {label_start}")

            self.intercode_generator.emit(f"{label_end}:")
        return action

    def handle_if(self, condition_data, if_body, else_body):
        def action():
            cond_temp, real_condition = condition_data
            label_else = self.intercode_generator.new_label()
            label_end = self.intercode_generator.new_label()

            self.intercode_generator.emit(f"ifFalse {cond_temp} goto {label_else}")

            if real_condition():
                for stmt in if_body:
                    if callable(stmt):
                        stmt()
            self.intercode_generator.emit(f"goto {label_end}")

            self.intercode_generator.emit(f"{label_else}:")

            if not real_condition():
                for stmt in else_body:
                    if callable(stmt):
                        stmt()

            self.intercode_generator.emit(f"{label_end}:")
        return action

    def handle_method_declaration(self, name, body):
        def action():
            self.methods[name] = body
            print(f" Método '{name}' definido.")
        return action

    def handle_method_call(self, name):
        def action():
            if name in self.methods:
                for stmt in self.methods[name]:
                    if callable(stmt):
                        stmt()
            else:
                self.errors.encolar_error(f" Error: Método '{name}' no está definido.")
        return action

    def handle_switch(self, var_name, cases, default_body):
        def action():
            val = self._get_value(var_name)
            matched = False
            print(f"🔀 SWITCH sobre '{var_name}' con valor '{val}'")
            for case_val, body in cases:
                if val == case_val:
                    for stmt in body:
                        if callable(stmt):
                            stmt()
                    matched = True
                    break
            if not matched and default_body:
                for stmt in default_body:
                    if callable(stmt):
                        stmt()
        return action

    def handle_print(self, value):
        def action():
            val = self._get_value(value)
            print(f"Salida: {val}")
        return action

    def _save_iteration_state(self):
        temp_dir = tempfile.gettempdir()
        path = os.path.join(temp_dir, "tabla_simbolos_iteracion_historial.json")

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                historial = json.load(f)
        else:
            historial = []

        historial.append({
            "timestamp": datetime.now().isoformat(),
            "iteration": len(historial) + 1,
            "tabla": self.symbol_table.symbols
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4)
