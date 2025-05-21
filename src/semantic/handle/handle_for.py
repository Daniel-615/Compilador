def handle_for(self, init_stmt, condition_fn, update_stmt, body):
        def action():
            print("Iniciando ciclo FOR")
            init_stmt()

            start_label = self.intercode_generator.new_label()
            true_label = self.intercode_generator.new_label()
            end_label = self.intercode_generator.new_label()

            self.intercode_generator.emit(f"{start_label}:")
            self.intercode_generator.emit(f"if {condition_fn.__name__} goto {true_label}")
            self.intercode_generator.emit(f"goto {end_label}")
            self.intercode_generator.emit(f"{true_label}:")

            iteration = 0
            while condition_fn():
                iteration += 1
                print(f"Iteración #{iteration} del FOR")
                for i, stmt in enumerate(body):
                    if callable(stmt):
                        stmt()
                update_stmt()
                self._save_iteration_state()

            self.intercode_generator.emit(f"goto {start_label}")
            self.intercode_generator.emit(f"{end_label}:")
        return action