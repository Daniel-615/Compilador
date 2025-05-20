import json, os, tempfile
from datetime import datetime
from src.intercode.optimize.optimize import Optimize  

class Semantic:
    def __init__(self, symbol_table, errors, lexer, interCodeGenerator):
        self.symbol_table = symbol_table
        self.errors = errors
        self.lexer = lexer
        self.methods = {}
        self.intercode_generator = interCodeGenerator

    def handle_declaration(self, name, var_type, scope, value=None):
        def action():
            evaluated_value = value if isinstance(value, (int, float, bool, str)) else self._get_value(value)
            self.symbol_table.add_symbol(name, var_type, scope, evaluated_value)
            print(f"Declaración: {name} = {evaluated_value}")
        action._is_declaration = True  # 👈 Marca la función
        return action


    def handle_assignment(self, name, value):
        def action():
            print(f"Recibido en asignación para '{name}': {value}")
            try:
                value_eval = None

                # 🔁 Resolver recursivamente cualquier tupla de expresiones anidadas
                def resolve_expr(val):
                    if isinstance(val, tuple) and len(val) == 3:
                        left, op, right = val
                        left_val = resolve_expr(left)
                        right_val = resolve_expr(right)

                        if left_val is None or right_val is None:
                            self.errors.encolar_error(f"Error: Subexpresión inválida: ({left} {op} {right})")
                            return None

                        return self.handle_expression(left_val, op, right_val)
                    elif isinstance(val, str):
                        fetched = self.symbol_table.get_symbol(val)
                        if fetched is None:
                            self.errors.encolar_error(f"Error: Variable '{val}' no tiene valor válido.")
                        return fetched
                    return val

                if isinstance(value, tuple):
                    # Evaluación real
                    resolved = resolve_expr(value)
                    value_eval = resolved

                    # Código intermedio textual (representación simbólica de la operación)
                    def expr_to_str(expr):
                        if isinstance(expr, tuple):
                            return f"({expr_to_str(expr[0])} {expr[1]} {expr_to_str(expr[2])})"
                        return str(expr)

                    temp = self.intercode_generator.new_temp()
                    self.intercode_generator.emit(f"{temp} = {expr_to_str(value)}")
                    self.intercode_generator.emit(f"{name} = {temp}")
                else:
                    value_eval = self._get_value(value)
                    self.intercode_generator.emit(f"{name} = {value}")

                print(f"📥 Resuelto '{name}' como valor final: {value_eval}")

                if self.symbol_table.get_symbol(name) is not None:
                    self.symbol_table.update_symbol(name, value_eval)
                    print(f"Asignación: {name} = {value_eval}")
                else:
                    self.errors.encolar_error(f"Error: Variable '{name}' no declarada.")
            except Exception as e:
                self.errors.encolar_error(f"Error al asignar a '{name}': {e}")
                print(f"Error general al asignar a '{name}': {e}")
        return action




    def handle_expression(self, left, operator, right):
        val1 = self._get_value(left)
        val2 = self._get_value(right)
        if val1 is None or val2 is None:
            self.errors.encolar_error(f" Error: Operación inválida: {left} {operator} {right}")
            return None
        result = self._apply_operator(val1, operator, val2)
        print(f"Evaluación: {val1} {operator} {val2} = {result}")
        return result

    def handle_term(self, left, operator, right):
        return self.handle_expression(left, operator, right)

    def handle_factor(self, value):
        return value  



    def _get_value(self, item):
        if isinstance(item, (int, float, bool)):
            return item  
        if isinstance(item, str):
            value = self.symbol_table.get_symbol(item)
            if value is None:
                self.errors.encolar_error(f"Error: Variable '{item}' no tiene un valor válido (None).")
            return value
        return item


    def _apply_operator(self, a, op, b):
        try:
            if a is None or b is None:
                self.errors.encolar_error(f"Error: Operación inválida entre {a} y {b}")
                return None
            if op == 'cristiano':
                return a + b if type(a) == type(b) else self._op_error(op, a, b)
            if op == 'tchouameni':
                return a - b if self._check_numeric(a, b) else self._op_error(op, a, b)
            if op == 'messi':
                return a * b if self._check_numeric(a, b) else self._op_error(op, a, b)
            if op == 'pepe':
                if b == 0:
                    self.errors.encolar_error("Error: División por cero.")
                    return None
                return a / b if self._check_numeric(a, b) else self._op_error(op, a, b)
        except Exception as e:
            self.errors.encolar_error(f"Error en operación: {e}")
        self.errors.encolar_error(f"Operador no válido: {op}")
        return None

    def _check_numeric(self, a, b):
        return isinstance(a, (int, float)) and isinstance(b, (int, float))

    def _op_error(self, op, a, b):
        self.errors.encolar_error(f" No se puede aplicar '{op}' entre {type(a).__name__} y {type(b).__name__}")
        return None

    def evaluate_condition_dynamic(self, left, op, right):
        def safe_get(val):
            return self.symbol_table.get_symbol(val) if isinstance(val, str) else val


        def condition():
            val1 = safe_get(left)
            val2 = safe_get(right)
            try:
                result = eval(f"{val1} {op} {val2}")
                print(f"Evaluando condición: {val1} {op} {val2} → {result}")
                return result
            except Exception as e:
                self.errors.encolar_error(f"Condición inválida: {left} {op} {right} → {e}")
                return False

        return condition

    def handle_for(self, init_stmt, condition_fn, update_stmt, body):
        def action():
            print("Iniciando ciclo FOR")
            init_stmt()

            start_label = self.intercode_generator.new_label()
            true_label = self.intercode_generator.new_label()
            end_label = self.intercode_generator.new_label()

            self.intercode_generator.emit(f"{start_label}:")
            self.intercode_generator.emit(f"if {condition_fn.__name__} goto {true_label}")
            self.intercode_generator.emit(f"goto {end_label}")
            self.intercode_generator.emit(f"{true_label}:")

            iteration = 0
            while condition_fn():
                iteration += 1
                print(f"Iteración #{iteration} del FOR")
                for i, stmt in enumerate(body):
                    if callable(stmt):
                        stmt()
                update_stmt()
                self._save_iteration_state()

            self.intercode_generator.emit(f"goto {start_label}")
            self.intercode_generator.emit(f"{end_label}:")
        return action

    def handle_do_while(self, condition_fn, body):
        def action():
            print("Iniciando ciclo DO-WHILE")
            start_label = self.intercode_generator.new_label()
            self.intercode_generator.emit(f"{start_label}:")

            iteration = 0
            while True:
                iteration += 1
                print(f"Iteración #{iteration} del DO-WHILE")
                for i, stmt in enumerate(body):
                    if callable(stmt):
                        stmt()
                self._save_iteration_state()

                if not condition_fn():
                    break
            self.intercode_generator.emit(f"if condition goto {start_label}")
        return action

    def handle_while(self, condition_fn, body):
        def action():
            print("Iniciando ciclo WHILE")
            start_label = self.intercode_generator.new_label()
            true_label = self.intercode_generator.new_label()
            end_label = self.intercode_generator.new_label()

            self.intercode_generator.emit(f"{start_label}:")
            self.intercode_generator.emit(f"if {condition_fn.__name__} goto {true_label}")
            self.intercode_generator.emit(f"goto {end_label}")
            self.intercode_generator.emit(f"{true_label}:")

            iteration = 0
            try:
                while condition_fn():
                    iteration += 1
                    print(f"Iteración #{iteration} del WHILE")
                    for i, stmt in enumerate(body):
                        if callable(stmt):
                            stmt()
                    self._save_iteration_state()
            except Exception as e:
                self.errors.encolar_error(f"Error en ejecución de cuerpo WHILE: {e}")
                print(f"Error en ejecución de cuerpo WHILE: {e}")

            self.intercode_generator.emit(f"goto {start_label}")
            self.intercode_generator.emit(f"{end_label}:")
        return action

    def handle_method_declaration(self, name, body):
        def action():
            self.methods[name] = body
            print(f"Método '{name}' definido.")
        action._is_declaration = True  # 👈 Marca como declaración
        return action


    def handle_method_call(self, name):
        def action():
            if name in self.methods:
                print(f"Llamando a método '{name}'...")
                for stmt in self.methods[name]:
                    if callable(stmt):
                        stmt()
            else:
                self.errors.encolar_error(f"Error: Método '{name}' no está definido.")
        return action

    def handle_if(self, condition_fn, if_body, else_body):
        def action():
            print("Iniciando IF con código intermedio")

            true_label = self.intercode_generator.new_label()
            false_label = self.intercode_generator.new_label()
            end_label = self.intercode_generator.new_label()

            # Emitir evaluación de condición
            self.intercode_generator.emit(f"if {condition_fn.__name__} goto {true_label}")
            self.intercode_generator.emit(f"goto {false_label}")

            # Bloque IF verdadero
            self.intercode_generator.emit(f"{true_label}:")
            if condition_fn():
                for stmt in if_body:
                    if callable(stmt):
                        stmt()
            self.intercode_generator.emit(f"goto {end_label}")

            # Bloque ELSE
            self.intercode_generator.emit(f"{false_label}:")
            if else_body:
                for stmt in else_body:
                    if callable(stmt):
                        stmt()

            # Fin del IF
            self.intercode_generator.emit(f"{end_label}:")
        return action

    def handle_switch(self, var_name, cases, default_body):
        def action():
            print("Iniciando SWITCH con código intermedio")

            val = self._get_value(var_name)
            if val is None:
                self.errors.encolar_error(f"Error: Variable '{var_name}' no tiene valor para SWITCH.")
                return

            end_label = self.intercode_generator.new_label()
            case_labels = [self.intercode_generator.new_label() for _ in cases]
            default_label = self.intercode_generator.new_label()

            # Comparaciones
            for (i, (case_val, _)) in enumerate(cases):
                self.intercode_generator.emit(f"if {var_name} == {case_val} goto {case_labels[i]}")

            self.intercode_generator.emit(f"goto {default_label}")

            # Bloques de cada case
            for (i, (case_val, body)) in enumerate(cases):
                self.intercode_generator.emit(f"{case_labels[i]}:")
                for stmt in body:
                    if callable(stmt):
                        stmt()
                self.intercode_generator.emit(f"goto {end_label}")  # <- simula break con un salto al final

            # Bloque default
            self.intercode_generator.emit(f"{default_label}:")
            if default_body:
                for stmt in default_body:
                    if callable(stmt):
                        stmt()

            self.intercode_generator.emit(f"{end_label}:")
        return action

    def handle_break(self):
        def action():
            print("Generando break")
            end_label = "END_SWITCH_LABEL" 
            self.intercode_generator.emit(f"goto {end_label}")
        return action


    def handle_print(self, value):
        def action():
            val = self._get_value(value)
            print(f"Salida: {val}")
        return action
    def getInterCode(self):
        return self.intercode_generator.code
    def optimize_intermediate_code(self):

        print("🛠️ Ejecutando optimización del código intermedio...")
        optimizer = Optimize(self.intercode_generator.code)  # el IR generado
        optimizer.optimize()

        # Reemplazamos el código intermedio antiguo con el optimizado
        self.intercode_generator.code = optimizer.get_optimized_ir()
        print("Código intermedio optimizado.")



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
           "tabla": {
                "global": self.symbol_table.global_scope,
                "local_scopes": self.symbol_table.scope_stack
            }
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4)
