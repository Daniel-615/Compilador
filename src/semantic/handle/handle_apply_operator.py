def _apply_operator(self, a, op, b):
        try:
            if a is None or b is None:
                self.errors.encolar_error(f"Error: Operación inválida entre {a} y {b}")
                return None
            if op == 'cristiano':
                return a + b if type(a) == type(b) else self._op_error(op, a, b)
            if op == 'tchouameni':
                return a - b if self._check_numeric(a, b) else self._op_error(op, a, b)
            if op == 'messi':
                return a * b if self._check_numeric(a, b) else self._op_error(op, a, b)
            if op == 'pepe':
                if b == 0:
                    self.errors.encolar_error("Error: División por cero.")
                    return None
                return a / b if self._check_numeric(a, b) else self._op_error(op, a, b)
        except Exception as e:
            self.errors.encolar_error(f"Error en operación: {e}")
        self.errors.encolar_error(f"Operador no válido: {op}")
        return None