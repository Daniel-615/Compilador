def handle_for(self, init_stmt, condition_fn, update_stmt, body):
    def action():
        print("Iniciando ciclo FOR")

        # Ejecutar la inicialización del ciclo
        init_stmt()

        # Registrar condición con nombre único basado en el nombre de la función
        base_name = condition_fn.__name__ if hasattr(condition_fn, "__name__") else "cond"
        cond_name = self.intercode_generator.get_cond_index(base_name)
        self.intercode_generator.register_condition(cond_name, condition_fn)

        # Generar etiquetas para el ciclo
        start_label = self.intercode_generator.new_label()
        body_label = self.intercode_generator.new_label()
        end_label = self.intercode_generator.new_label()

        self.intercode_generator.emit(f"// INICIO FOR")
        self.intercode_generator.emit(f"{start_label}:")
        self.intercode_generator.emit(f"if {cond_name} goto {body_label}")
        self.intercode_generator.emit(f"goto {end_label}")
        self.intercode_generator.emit(f"{body_label}:")

        iteration = 0
        while condition_fn():
            iteration += 1
            print(f"Iteración #{iteration} del FOR")
            self.symbol_table.enter_scope()
            for stmt in body:
                if callable(stmt):
                    stmt()
            self.symbol_table.exit_scope()

            # Ejecutar actualización del ciclo (por ejemplo, i = i + 1)
            update_stmt()
            self._save_iteration_state()

        self.intercode_generator.emit(f"goto {start_label}")
        self.intercode_generator.emit(f"{end_label}:")
        self.intercode_generator.emit(f"// FIN FOR")

    return action
