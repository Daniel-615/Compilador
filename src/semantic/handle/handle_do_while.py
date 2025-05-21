def handle_do_while(self, condition_fn, body):
        def action():
            print("Iniciando ciclo DO-WHILE")
            start_label = self.intercode_generator.new_label()
            self.intercode_generator.emit(f"{start_label}:")

            iteration = 0
            while True:
                iteration += 1
                print(f"Iteración #{iteration} del DO-WHILE")
                for i, stmt in enumerate(body):
                    if callable(stmt):
                        stmt()
                self._save_iteration_state()

                if not condition_fn():
                    break
            self.intercode_generator.emit(f"if condition goto {start_label}")
        return action