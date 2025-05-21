def handle_declaration(self, name, var_type, scope, value=None):
        def action():
            evaluated_value = value if isinstance(value, (int, float, bool, str)) else self._get_value(value)
            self.symbol_table.add_symbol(name, var_type, scope, evaluated_value)
            print(f"Declaración: {name} = {evaluated_value}")
        return action