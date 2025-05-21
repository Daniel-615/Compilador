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
            self.errors.encolar_error(f"Error interno: el nombre del método debe ser string, recibido {type(name)}")
            print(f"❌ Nombre de método inválido: {name}")
            return

        flat_body = flatten(body)
        self.methods[name] = flat_body
        print(f"Método '{name}' definido.")
    return action
