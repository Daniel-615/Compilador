def evaluate_condition_dynamic(self, left, op, right):
    def condition_fn():
        # Obtener valores reales
        left_sym = self.symbol_table.get_symbol(left)
        if left_sym is None:
            self.errors.encolar_error(f"Error: Variable '{left}' no declarada en la condición.")
            condition_fn.temp_result = "0"
            return False

        left_val = left_sym['value']
        right_val = self._get_value(right)

        if left_val is None or right_val is None:
            self.errors.encolar_error("Error: condición con operandos no evaluables.")
            condition_fn.temp_result = "0"
            return False

        # Generar el temporal para código intermedio
        temp = self.intercode_generator.new_temp()
        self.intercode_generator.emit(f"{temp} = {left} {op} {right}")
        condition_fn.temp_result = temp  # Guardamos el temporal para emitir luego: if !temp goto

        # Evaluación booleana inmediata para el flujo lógico
        try:
            if op == '>':
                return left_val > right_val
            elif op == '<':
                return left_val < right_val
            elif op == '==':
                return left_val == right_val
            elif op == '!=':
                return left_val != right_val
            elif op == '>=':
                return left_val >= right_val
            elif op == '<=':
                return left_val <= right_val
            else:
                self.errors.encolar_error(f"Operador relacional no soportado: {op}")
                return False
        except Exception as e:
            self.errors.encolar_error(f"Error en evaluación de condición: {e}")
            return False

    return condition_fn
