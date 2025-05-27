def handle_if(self, condition_fn, if_body, else_body):
    def action():
        print("Iniciando IF con código intermedio")

        true_label = self.intercode_generator.new_label()
        false_label = self.intercode_generator.new_label()
        end_label = self.intercode_generator.new_label()

        self.intercode_generator.emit("// INICIO IF")

        condition_result = condition_fn()
        cond_temp = condition_fn.temp_result
        self.intercode_generator.emit(f"if !({cond_temp}) goto {false_label}")
        
        # Bloque IF verdadero
        for stmt in if_body:
            if callable(stmt):
                stmt()
        self.intercode_generator.emit(f"goto {end_label}")

        # Bloque ELSE
        self.intercode_generator.emit(f"{false_label}:")
        if else_body:
            self.intercode_generator.emit("// ELSE")
            for stmt in else_body:
                if callable(stmt):
                    stmt()

        self.intercode_generator.emit(f"{end_label}:")
        self.intercode_generator.emit("// FIN IF")

    return action
