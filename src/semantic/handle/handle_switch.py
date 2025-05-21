def handle_switch(self, var_name, cases, default_body):
    def action():
        print("📦 Iniciando SWITCH con código intermedio")
        print("🧪 Verificando estructura de 'cases':")

        processed_cases = []
        for i, case in enumerate(cases):
            print(f"  👉 case #{i}: {case} | tipo={type(case)}")

            # Asegurar que cada case sea una tupla (valor, [body])
            if not isinstance(case, tuple) or len(case) != 2:
                self.errors.encolar_error(f"❌ Error: el case #{i} no tiene una estructura válida (valor, cuerpo).")
                return

            val, body = case

            # Validar que el valor sea hashable (para evitar errores tipo 'list')
            try:
                hash(val)
            except TypeError:
                self.errors.encolar_error(f"❌ Error: el valor del case #{i} no es válido para comparación: {val}")
                return

            # Asegurar que el body sea una lista
            if not isinstance(body, list):
                body = [body]

            processed_cases.append((val, body))

        print("✅ Casos del switch procesados como tuplas:", processed_cases)

        # Preparar etiquetas
        end_label = self.intercode_generator.new_label()
        case_labels = [self.intercode_generator.new_label() for _ in processed_cases]
        default_label = self.intercode_generator.new_label()

        # Emitir condiciones
        for i, (case_val, _) in enumerate(processed_cases):
            self.intercode_generator.emit(f"if {var_name} == {repr(case_val)} goto {case_labels[i]}")

        self.intercode_generator.emit(f"goto {default_label}")

        # Emitir código de cada case
        for i, (case_val, body) in enumerate(processed_cases):
            self.intercode_generator.emit(f"{case_labels[i]}:")
            for stmt in body:
                if callable(stmt):
                    stmt()
            self.intercode_generator.emit(f"goto {end_label}")
        
        # Emitir bloque default
        self.intercode_generator.emit(f"{default_label}:")
        if default_body:
            for stmt in default_body:
                if callable(stmt):
                    stmt()

        self.intercode_generator.emit(f"{end_label}:")

    return action
