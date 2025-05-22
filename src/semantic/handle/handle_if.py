def handle_if(self, condition_fn, if_body, else_body):
    def action():
        print("Iniciando IF con código intermedio")

        cond_name = f"cond_if_{self.intercode_generator.get_cond_index('if')}"
        self.intercode_generator.register_condition(cond_name, condition_fn)

        true_label = self.intercode_generator.new_label()
        false_label = self.intercode_generator.new_label()
        end_label = self.intercode_generator.new_label()

        # Comentario de inicio
        self.intercode_generator.emit("// INICIO IF")

        # Evaluar condición
        self.intercode_generator.emit(f"if {cond_name} goto {true_label}")
        self.intercode_generator.emit(f"goto {false_label}")

        # Bloque IF verdadero
        self.intercode_generator.emit(f"{true_label}:")
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

        # Cierre
        self.intercode_generator.emit(f"{end_label}:")
        self.intercode_generator.emit("// FIN IF")

    return action
