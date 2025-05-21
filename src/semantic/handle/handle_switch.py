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