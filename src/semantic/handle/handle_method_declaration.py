def handle_method_declaration(self, name, body):
    def flatten(statements):
        flat = []
        for stmt in statements:
            if isinstance(stmt, list):
                flat.extend(flatten(stmt))
            else:
                flat.append(stmt)
        return flat

    def action():
        if not isinstance(name, str):
            self.errors.encolar_error(
                f"Error interno: el nombre del método debe ser string, recibido {type(name)}"
            )
            print(f"Nombre de método inválido: {name}")
            return

        flat_body = flatten(body)
        self.methods[name] = flat_body

        # Emitir inicio de función
        self.intercode_generator.emit(f"function {name}:")

        # Iniciar nuevo ámbito local
        self.symbol_table.enter_scope()
        self.en_funcion = True

        for i, stmt in enumerate(flat_body):
            if callable(stmt):
                print(f"Ejecutando instrucción {i} de '{name}'")
                stmt()

        self.en_funcion = False
        self.symbol_table.exit_scope()

        # Emitir cierre de función
        self.intercode_generator.emit("end")

        print(f"Método '{name}' definido y procesado con código intermedio.")
    return action
