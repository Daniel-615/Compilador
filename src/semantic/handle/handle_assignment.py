def handle_assignment(self, name, value):
    def action():
        print(f"Recibido en asignación para '{name}': {value}")
        try:
            value_eval = None

            if isinstance(value, tuple):
                if len(value) == 3:
                    left, op, right = value
                    left_val = self._get_value(left)
                    right_val = self._get_value(right)

                    if left_val is None or right_val is None:
                        self.errors.encolar_error(f"Error: No se puede operar porque '{left}' o '{right}' es None. Asignación a '{name}' no realizada.")
                        print(f"Asignación cancelada para '{name}' por valores inválidos.")
                        return

                    temp = self.intercode_generator.new_temp()
                    self.intercode_generator.emit(f"{temp} = {left} {op} {right}")
                    self.intercode_generator.emit(f"{name} = {temp}")

                    value_eval = self.handle_expression(left, op, right)
                else:
                    self.errors.encolar_error(f"Error: La expresión para '{name}' debe tener 3 elementos (left, op, right).")
                    print(f"Tupla inválida para '{name}': {value}")
                    return
            else:
                value_eval = self._get_value(value)
                self.intercode_generator.emit(f"{name} = {value}")

            if self.symbol_table.get_symbol(name) is not None:
                self.symbol_table.update_symbol(name, value_eval)
                print(f"Asignación: {name} = {value_eval}")
            else:
                self.errors.encolar_error(f"Error: Variable '{name}' no declarada.")
        except Exception as e:
            self.errors.encolar_error(f"Error al asignar a '{name}': {e}")
            print(f"Error general al asignar a '{name}': {e}")
    return action
