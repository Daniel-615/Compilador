def _get_value(self, item):
    if isinstance(item, str):
        symbol = self.symbol_table.get_symbol(item)
        if symbol is None:
            self.errors.encolar_error(f"Error: Variable '{item}' no ha sido declarada.")
            return None
        return symbol['value']
    return item
