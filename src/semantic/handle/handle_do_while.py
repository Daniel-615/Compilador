def handle_do_while(self, condition_fn, body):
    def action():
        print("Iniciando ciclo DO-WHILE")
        start_label = self.intercode_generator.new_label()

        self.intercode_generator.emit(f"//INICIO DO-WHILE")
        self.intercode_generator.emit(f"{start_label}:")

        iteration = 0
        while True:
            iteration += 1
            print(f"Iteración #{iteration} del DO-WHILE")

            self.symbol_table.enter_scope()
            for stmt in body:
                if callable(stmt):
                    stmt()
            self.symbol_table.exit_scope()
            self._save_iteration_state()

            if not condition_fn():
                break

        cond_label = condition_fn.__name__ if hasattr(condition_fn, "__name__") else "condicion"
        self.intercode_generator.emit(f"if {cond_label} goto {start_label}")
        self.intercode_generator.emit(f"//FIN DO-WHILE")

    return action