import time
from threading import Event
import json, os, tempfile
from datetime import datetime
class Semantic:
    def __init__(self, symbol_table, errors, lexer,intercode_generator):
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
                value_eval = None

                if isinstance(value, tuple):
                    # Si es una expresión tipo (left, op, right)
                    if len(value) == 3:
                        value_eval = self.handle_expression(*value)
                        
                    else:
                        self.errors.encolar_error(f" Error: La expresión para '{name}' debe tener 3 elementos (left, op, right), pero tiene {len(value)}.")
                        print(f" Tupla inválida para '{name}': {value}")
                        return
                else:
                    # Si es un valor literal o una variable
                    value_eval = self._get_value(value)

                # Verifica si la variable está declarada
                if self.symbol_table.get_symbol(name) is not None:
                    self.symbol_table.update_symbol(name, value_eval)
                    print(f"Asignación: {name} = {value_eval}")

                    #  Código intermedio: asignación directa
                    self.intercode_generator.emit(f"{name} = {value_eval}")
                else:
                    self.errors.encolar_error(f" Error: Variable '{name}' no declarada.")
            except Exception as e:
                self.errors.encolar_error(f" Error al asignar a '{name}': {e}")
                print(f" Error al asignar a '{name}': {e}")
        return action


    #codigo intermedio operadores
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
        return temp  # Regresa el temporal generado

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
                    self.errors.encolar_error(" Error: División por cero.")
                    return None
                return a / b if self._check_numeric(a, b) else self._op_error(op, a, b)
        except Exception as e:
            self.errors.encolar_error(f" Error en operación: {e}")
        self.errors.encolar_error(f" Operador no válido: {op}")
        return None

    def _check_numeric(self, a, b):
        return isinstance(a, (int, float)) and isinstance(b, (int, float))

    def _op_error(self, op, a, b):
        self.errors.encolar_error(f" No se puede aplicar '{op}' entre {type(a).__name__} y {type(b).__name__}")
        return None

    def evaluate_condition_dynamic(self, left, op, right):
        def safe_get(val):
            return self.symbol_table.get_symbol(val) if isinstance(val, str) and val in self.symbol_table.symbols else val

        def condition():
            val1 = safe_get(left)
            val2 = safe_get(right)
            try:
                result = eval(f"{val1} {op} {val2}")
                print(f" Evaluando condición: {val1} {op} {val2} → {result}")
                return result
            except Exception as e:
                self.errors.encolar_error(f" Condición inválida: {left} {op} {right} → {e}")
                return False

        return condition
    #for (RAMOS)
    def handle_for(self, init_stmt, condition_fn, update_stmt, body):
        def action():
            print(" Iniciando ciclo FOR")
            iteration = 0
            init_stmt()  # Ejecuta la inicialización
            while condition_fn():
                iteration += 1
                print(f" Iteración #{iteration} del FOR")
                for i, stmt in enumerate(body):
                    if callable(stmt):
                        stmt()
                update_stmt()  # Ejecuta el update después del cuerpo
                self._save_iteration_state()
        return action

    #do while (aguero ,walker)
    def handle_do_while(self, condition_fn, body):
        def action():
            print(" Iniciando ciclo DO-WHILE")
            iteration = 0
            while True:
                iteration += 1
                print(f" Iteración #{iteration} del DO-WHILE")
                for i, stmt in enumerate(body):
                    if callable(stmt):
                        stmt()
                self._save_iteration_state()
                if not condition_fn():
                    break
        return action

    #while (walker)
    def handle_while(self, condition_fn, body):
        def action():
            print(f" WHILE detectado, cuerpo recibido: {body}")
            iteration = 0
            try:
                print(condition_fn.__name__)
                while condition_fn():
                    iteration += 1
                    print(f" Iteración #{iteration} del WHILE")
                    print(f"[DEBUG] Tipo de body: {type(body)}")
                    for i, stmt in enumerate(body):
                        try:
                            if callable(stmt):
                                print(f" Ejecutando instrucción #{i+1} del cuerpo...")
                                stmt()
                            else:
                                print(f" Instrucción #{i+1} no es callable: {stmt}")
                        except Exception as inner_err:
                            self.errors.encolar_error(f"Error al ejecutar instrucción #{i+1} del WHILE: {inner_err}")
                            print(f" Error en instrucción #{i+1}: {inner_err}")
                    self._save_iteration_state()
            except Exception as e:
                self.errors.encolar_error(f" Error general en el cuerpo del WHILE: {e}")
                print(f" Error general en el cuerpo del WHILE: {e}")
        return action

    def handle_method_declaration(self, name, body):
        def action():
            self.methods[name] = body
            print(f" Método '{name}' definido.")
        return action

    def handle_method_call(self, name):
        def action():
            if name in self.methods:
                print(f" Llamando a método '{name}'...")
                for stmt in self.methods[name]:
                    if callable(stmt):
                        stmt()
            else:
                self.errors.encolar_error(f" Error: Método '{name}' no está definido.")
        return action
    #estructuras de control
    #if, else
    def handle_if(self, condition_fn, if_body, else_body):
        def action():
            if condition_fn():
                print(" IF verdadero: ejecutando bloque")
                for stmt in if_body:
                    if callable(stmt):
                        stmt()
            else:
                print(" IF falso: ejecutando ELSE")
                for stmt in else_body:
                    if callable(stmt):
                        stmt()
        return action
    #swich
    def handle_switch(self, var_name, cases, default_body):
        def action():
            val = self._get_value(var_name)
            matched = False
            print(f"🔀 SWITCH sobre '{var_name}' con valor '{val}'")
            for case_val, body in cases:
                if val == case_val:
                    print(f"🎯 Coincidencia con CASE: {case_val}")
                    for stmt in body:
                        if callable(stmt):
                            stmt()
                    matched = True
                    break
            if not matched and default_body:
                print(f"⚠️ Ejecutando bloque DEFAULT")
                for stmt in default_body:
                    if callable(stmt):
                        stmt()
        return action
    #impresion en pantalla 
    def handle_print(self, value):
        def action():
            val = self._get_value(value)
            print(f"Salida: {val}")
        return action

    def _save_iteration_state(self):
        temp_dir = tempfile.gettempdir()
        path = os.path.join(temp_dir, "tabla_simbolos_iteracion_historial.json")

        # Cargar historial anterior (si existe)
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

