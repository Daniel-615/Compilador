def _get_value(self, item):
        if isinstance(item, str):
            value = self.symbol_table.get_symbol(item)
            if value is None:
                self.errors.encolar_error(f"Error: Variable '{item}' no tiene un valor válido (None).")
            return value
        return item