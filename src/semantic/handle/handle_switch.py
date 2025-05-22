def handle_switch(self, var_name, cases, default_body):
    def action():
        print("Iniciando SWITCH con código intermedio")
        print("Verificando estructura de 'cases':")

        processed_cases = []
        for i, case in enumerate(cases):
            print(f"case #{i}: {case} | tipo={type(case)}")

            if not isinstance(case, tuple) or len(case) != 2:
                self.errors.encolar_error(f"Error: el case #{i} no tiene una estructura válida (valor, cuerpo).")
                return

            val, body = case

            try:
                hash(val)
            except TypeError:
                self.errors.encolar_error(f"Error: el valor del case #{i} no es válido para comparación: {val}")
                return

            if not isinstance(body, list):
                body = [body]

            processed_cases.append((val, body))

        print("Casos del switch procesados como tuplas:", processed_cases)

        # Emitir un marcador para que el generador C++ detecte que debe generar un switch real
        self.intercode_generator.emit(f"// SWITCH_START {var_name}")

        for val, body in processed_cases:
            self.intercode_generator.emit(f"// CASE {repr(val)}")
            for stmt in body:
                if callable(stmt):
                    stmt()
            self.intercode_generator.emit("// BREAK")

        self.intercode_generator.emit(f"// DEFAULT")
        if default_body:
            for stmt in default_body:
                if callable(stmt):
                    stmt()

        self.intercode_generator.emit(f"// SWITCH_END")

    return action
