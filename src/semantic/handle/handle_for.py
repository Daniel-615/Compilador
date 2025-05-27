def handle_for(self, init_stmt, condition_fn, update_stmt, body):
    def action():
        print("Iniciando ciclo FOR")

        # Ejecutar inicialización (ej: x = 0)
        init_stmt()

        # Generar etiquetas
        start_label = self.intercode_generator.new_label()
        body_label = self.intercode_generator.new_label()
        end_label = self.intercode_generator.new_label()

        self.intercode_generator.emit(f"// INICIO FOR")
        self.intercode_generator.emit(f"{start_label}:")

        # Evaluar condición y generar temporal
        condition_result = condition_fn()
        cond_temp = condition_fn.temp_result
        self.intercode_generator.emit(f"if !({cond_temp}) goto {end_label}")
        self.intercode_generator.emit(f"{body_label}:")

        iteration = 0
        while condition_result:
            iteration += 1
            print(f"Iteración #{iteration} del FOR")
            self.symbol_table.enter_scope()

            for stmt in body:
                if callable(stmt):
                    stmt()
            self.symbol_table.exit_scope()

            update_stmt()
            self._save_iteration_state()

            # Volver a evaluar la condición en cada iteración
            condition_result = condition_fn()
            cond_temp = condition_fn.temp_result
            self.intercode_generator.emit(f"if !({cond_temp}) goto {end_label}")
            self.intercode_generator.emit(f"goto {body_label}")

        # Cierre del ciclo
        self.intercode_generator.emit(f"{end_label}:")
        self.intercode_generator.emit(f"// FIN FOR")

    return action
