def handle_do_while(self, condition_fn, body):
    def action():
        print("Iniciando ciclo DO-WHILE")

        # Crear etiqueta de inicio del ciclo
        start_label = self.intercode_generator.new_label()
        self.intercode_generator.emit(f"//INICIO DO-WHILE")
        self.intercode_generator.emit(f"{start_label}:")

        # Ejecutar el cuerpo del ciclo al menos una vez
        iteration = 0
        self.symbol_table.enter_scope()
        for stmt in body:
            if callable(stmt):
                stmt()
        self.symbol_table.exit_scope()
        self._save_iteration_state()

        # Evaluar la condición una sola vez al final
        condition_result = condition_fn()
        cond_temp = condition_fn.temp_result
        self.intercode_generator.emit(f"if ({cond_temp}) goto {start_label}")
        self.intercode_generator.emit(f"//FIN DO-WHILE")

    return action
