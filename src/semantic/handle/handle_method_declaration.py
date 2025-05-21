def handle_method_declaration(self, name, body):
        def action():
            self.methods[name] = body
            print(f"Método '{name}' definido.")
        return action