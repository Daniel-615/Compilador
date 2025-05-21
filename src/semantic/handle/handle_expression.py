def handle_expression(self, left, operator, right):
    def action():
        val1 = self._get_value(left)
        val2 = self._get_value(right)
        if val1 is None or val2 is None:
            self.errors.encolar_error(f" Error: Operación inválida: {left} {operator} {right}")
            return None
        result = self._apply_operator(val1, operator, val2)
        print(f"Evaluación: {val1} {operator} {val2} = {result}")
        return result
    return action
