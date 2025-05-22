def handle_expression(self, left, operator, right):
    def action():
        # Obtener los operandos en forma de texto o temporales
        val1 = left if isinstance(left, (int, float, str)) else self._get_value(left)
        val2 = right if isinstance(right, (int, float, str)) else self._get_value(right)

        # Validación
        if val1 is None or val2 is None:
            self.errors.encolar_error(f"Error: Operación inválida: {left} {operator} {right}")
            return None

        # Crear un temporal y emitir instrucción
        temp = self.intercode_generator.new_temp()
        self.intercode_generator.emit(f"{temp} = {left} {operator} {right}")

        print(f"Evaluación simbólica: {temp} = {left} {operator} {right}")
        return temp  # Retorna el temporal para su uso posterior
    return action
