def handle_assignment(self, name, value):
    def action():
        print(f"Recibido en asignación para '{name}': {value}")
        try:
            value_eval = None

            # 🧠 Evaluar expresiones (tuplas) de manera recursiva
            def evaluar_exp(val):
                if isinstance(val, tuple) and len(val) == 3:
                    left, op, right = val
                    left_val = evaluar_exp(left)
                    right_val = evaluar_exp(right)
                    if left_val is None or right_val is None:
                        self.errors.encolar_error(
                            f"Error: No se puede operar porque '{left}' o '{right}' es None."
                        )
                        return None
                    result = self._apply_operator(left_val, op, right_val)
                    print(f"Evaluación: {left_val} {op} {right_val} = {result}")
                    return result
                elif callable(val):
                    return val()  # Ejecutar funciones como resultado de métodos
                else:
                    return self._get_value(val)

            # 🔧 Evaluar el valor final
            value_eval = evaluar_exp(value)

            if value_eval is None:
                self.errors.encolar_error(f"Error: Asignación a '{name}' fallida por valor inválido.")
                return

            # 🔨 Generar código intermedio
            if isinstance(value, tuple) and len(value) == 3:
                left, op, right = value
                temp = self.intercode_generator.new_temp()
                self.intercode_generator.emit(f"{temp} = {left} {op} {right}")
                self.intercode_generator.emit(f"{name} = {temp}")
            else:
                self.intercode_generator.emit(f"{name} = {value}")

            # 💾 Asignar en la tabla de símbolos
            if self.symbol_table.get_symbol(name) is not None:
                self.symbol_table.update_symbol(name, value_eval)
                print(f"Asignación: {name} = {value_eval}")
            else:
                self.errors.encolar_error(f"Error: Variable '{name}' no declarada.")

        except Exception as e:
            self.errors.encolar_error(f"Error al asignar a '{name}': {e}")
            print(f"Error general al asignar a '{name}': {e}")

    return action
