def evaluate_condition_dynamic(self, left, op, right):
        def safe_get(val):
            return self.symbol_table.get_symbol(val) if isinstance(val, str) and val in self.symbol_table.symbols else val

        def condition():
            val1 = safe_get(left)
            val2 = safe_get(right)
            try:
                result = eval(f"{val1} {op} {val2}")
                print(f"Evaluando condición: {val1} {op} {val2} → {result}")
                return result
            except Exception as e:
                self.errors.encolar_error(f"Condición inválida: {left} {op} {right} → {e}")
                return False

        return condition