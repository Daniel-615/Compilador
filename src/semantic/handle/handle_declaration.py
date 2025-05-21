def handle_declaration(self, name, var_type, scope=None, value=None):
    def action():
        actual_scope = 'local' if self.en_funcion else 'global'
        evaluated_value = value if isinstance(value, (int, float, bool, str)) else self._get_value(value)
        self.symbol_table.add_symbol(name, var_type, actual_scope, evaluated_value)
        print(f"Declaración ({actual_scope}): {name} = {evaluated_value}")
    return action
