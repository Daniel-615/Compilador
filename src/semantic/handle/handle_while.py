def handle_while(self, condition_fn, body):
        def action():
            print("Iniciando ciclo WHILE")
            start_label = self.intercode_generator.new_label()
            true_label = self.intercode_generator.new_label()
            end_label = self.intercode_generator.new_label()

            self.intercode_generator.emit(f"{start_label}:")
            self.intercode_generator.emit(f"if {condition_fn.__name__} goto {true_label}")
            self.intercode_generator.emit(f"goto {end_label}")
            self.intercode_generator.emit(f"{true_label}:")

            iteration = 0
            try:
                while condition_fn():
                    iteration += 1
                    print(f"Iteración #{iteration} del WHILE")
                    for i, stmt in enumerate(body):
                        if callable(stmt):
                            stmt()
                    self._save_iteration_state()
            except Exception as e:
                self.errors.encolar_error(f"Error en ejecución de cuerpo WHILE: {e}")
                print(f"Error en ejecución de cuerpo WHILE: {e}")

            self.intercode_generator.emit(f"goto {start_label}")
            self.intercode_generator.emit(f"{end_label}:")
        return action