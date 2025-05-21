def handle_method_call(self, name):
        def action():
            if name in self.methods:
                print(f"Llamando a método '{name}'...")
                for stmt in self.methods[name]:
                    if callable(stmt):
                        stmt()
            else:
                self.errors.encolar_error(f"Error: Método '{name}' no está definido.")
        return action