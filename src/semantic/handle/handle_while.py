def handle_while(self, condition_fn, body):
    def action():
        print("Iniciando ciclo WHILE")

        # Generar nombre único para la condición
        base_name = condition_fn.__name__ if hasattr(condition_fn, "__name__") else "cond"
        cond_name = self.intercode_generator.get_cond_index(base_name)
        self.intercode_generator.register_condition(cond_name, condition_fn)

        # Crear etiquetas
        start_label = self.intercode_generator.new_label()
        body_label = self.intercode_generator.new_label()
        end_label = self.intercode_generator.new_label()

        self.intercode_generator.emit(f"// INICIO WHILE")
        self.intercode_generator.emit(f"{start_label}:")
        self.intercode_generator.emit(f"if {cond_name} goto {body_label}")
        self.intercode_generator.emit(f"goto {end_label}")
        self.intercode_generator.emit(f"{body_label}:")

        # Ejecutar cuerpo del ciclo
        iteration = 0
        try:
            while condition_fn():
                iteration += 1
                print(f"Iteración #{iteration} del WHILE")
                self.symbol_table.enter_scope()
                for stmt in body:
                    if callable(stmt):
                        stmt()
                self.symbol_table.exit_scope()
                self._save_iteration_state()
        except Exception as e:
            self.errors.encolar_error(f"Error en cuerpo WHILE: {e}")
            print(f"Error en cuerpo WHILE: {e}")

        self.intercode_generator.emit(f"goto {start_label}")
        self.intercode_generator.emit(f"{end_label}:")
        self.intercode_generator.emit(f"// FIN WHILE")

    return action
