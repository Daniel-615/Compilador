def handle_method_call(self, name):
    def call_with_scope():
        if name not in self.methods:
            self.errors.encolar_error(f"Error: Método '{name}' no está definido.")
            return

        body = self.methods[name]
        print(f"👀 Ejecutando método '{name}', body = {body}")

        if not isinstance(body, list):
            self.errors.encolar_error(f"Error: El cuerpo del método '{name}' no es una lista.")
            return

        # 🟢 Entramos a contexto local
        self.symbol_table.enter_scope()
        self.en_funcion = True

        for i, stmt in enumerate(body):
            if not callable(stmt):
                self.errors.encolar_error(f"Error: El elemento {i} del método '{name}' no es ejecutable.")
                continue

            print(f"⚙️ Ejecutando instrucción {i} del método '{name}'")
            stmt()

        # 🔴 Salimos del contexto local
        self.en_funcion = False
        self.symbol_table.exit_scope()
    return call_with_scope
