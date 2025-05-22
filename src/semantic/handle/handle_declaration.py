def handle_declaration(self, name, var_type, scope=None, value=None):
    def action():
        actual_scope = 'local' if self.en_funcion else 'global'

        # Evaluar el valor inicial (literal o variable)
        if isinstance(value, (int, float, bool, str)):
            evaluated_value = value
        elif isinstance(value, tuple) and len(value) == 3:
            # Si es una expresión como (a, '+', b)
            left, op, right = value
            temp = self.intercode_generator.emit_temp(left, op, right)
            evaluated_value = temp
        else:
            evaluated_value = self._get_value(value)

        # Guardar en tabla de símbolos
        self.symbol_table.add_symbol(name, var_type, actual_scope, evaluated_value)
        print(f"Declaración ({actual_scope}): {name} = {evaluated_value}")

        # Generar código intermedio
        if evaluated_value is not None:
            self.intercode_generator.emit(f"{name} = {evaluated_value}")

    return action
