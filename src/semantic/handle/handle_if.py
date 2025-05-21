def handle_if(self, condition_fn, if_body, else_body):
        def action():
            print("Iniciando IF con código intermedio")

            true_label = self.intercode_generator.new_label()
            false_label = self.intercode_generator.new_label()
            end_label = self.intercode_generator.new_label()

            # Emitir evaluación de condición
            self.intercode_generator.emit(f"if {condition_fn.__name__} goto {true_label}")
            self.intercode_generator.emit(f"goto {false_label}")

            # Bloque IF verdadero
            self.intercode_generator.emit(f"{true_label}:")
            if condition_fn():
                for stmt in if_body:
                    if callable(stmt):
                        stmt()
            self.intercode_generator.emit(f"goto {end_label}")

            # Bloque ELSE
            self.intercode_generator.emit(f"{false_label}:")
            if else_body:
                for stmt in else_body:
                    if callable(stmt):
                        stmt()

            # Fin del IF
            self.intercode_generator.emit(f"{end_label}:")
        return action