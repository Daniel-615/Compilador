def p_error(self, p):
    if p:
        try:
            col = self.errors.find_column(p)
            row = self.errors.find_line(p)
            token = p.value.lower() if isinstance(p.value, str) else str(p.value)

            # 0. Revisión de línea anterior por posible falta de punto y coma
            if p.lexer and hasattr(p.lexer, 'lexdata'):
                prev_text = p.lexer.lexdata[:p.lexpos].splitlines()
                if prev_text:
                    prev_line = prev_text[-1].strip()
                    if (
                        prev_line and
                        not prev_line.endswith(';') and
                        ('=' in prev_line or any(kw in prev_line for kw in {'milito', 'zidane', 'saviola', 'valderrama', 'iniesta'}))
                    ):
                        self.errors.encolar_error(
                            f"Error: probablemente falta ';' al final de la línea anterior a '{token}' en fila {row}, col {col}."
                        )
                        return

            # 1. Estructuras de control
            if token == 'walker':
                self.errors.encolar_error(
                    f"Error: se esperaba '(' después de 'walker' en la fila {row} y columna {col}. "
                    f"¿Faltan los paréntesis con la condición?"
                )
            elif token == 'ballack':
                self.errors.encolar_error(
                    f"Error: se esperaba condición entre paréntesis después de 'ballack' en la fila {row}, col {col}."
                )
            elif token == 'robben':
                self.errors.encolar_error(
                    f"Error: 'robben' fuera de lugar en la fila {row}, col {col}. "
                    f"¿Está cerrando correctamente el 'if' anterior con '}}'?"
                )
            elif token == 'ramos':
                self.errors.encolar_error(
                    f"Error: for mal formado con 'ramos' en la fila {row}, col {col}. "
                    f"¿Faltan los ';' o los paréntesis con los parámetros del bucle?"
                )

            # 2. Switch-case
            elif token == 'son':
                self.errors.encolar_error(
                    f"Error: falta ':' después de 'son {p.value}' en la fila {row}, col {col}."
                )
            elif token == 'ronaldinho':
                self.errors.encolar_error(
                    f"Error: 'ronaldinho' debe usarse al final del switch en la fila {row}, col {col}."
                )
            elif token == 'forlan':
                self.errors.encolar_error(
                    f"Error: estructura de switch 'forlan' mal formada en fila {row}, col {col}. "
                    f"¿Faltan las llaves '{{}}' o los casos 'son X:'?"
                )

            # 3. Operadores sin operandos
            elif token in {'cristiano', 'tchouameni', 'messi', 'pepe'}:
                self.errors.encolar_error(
                    f"Error: operador '{token}' usado sin operandos válidos en fila {row}, col {col}."
                )

            # 4. Tipos sin identificador
            elif token in {'milito', 'zidane', 'saviola', 'iniesta', 'valderrama'}:
                self.errors.encolar_error(
                    f"Error: después del tipo '{token}' se esperaba un identificador en fila {row}, col {col}."
                )

            # 5. Literales mal cerrados
            elif token.startswith('"') or token.startswith("'"):
                self.errors.encolar_error(
                    f"Error: literal no cerrado correctamente en fila {row}, col {col}."
                )

            # 6. Paréntesis y llaves
            elif token == '{':
                self.errors.encolar_error(
                    f"Error: bloque '{{' mal ubicado o sin estructura anterior válida en fila {row}, col {col}."
                )
            elif token == '}':
                self.errors.encolar_error(
                    f"Error: llave de cierre '}}' sin apertura correspondiente en fila {row}, col {col}."
                )
            elif token == '(':
                self.errors.encolar_error(
                    f"Error: paréntesis de apertura '(' sin cierre en fila {row}, col {col}."
                )
            elif token == ')':
                self.errors.encolar_error(
                    f"Error: paréntesis de cierre ')' sin apertura en fila {row}, col {col}."
                )

            # 7. Uso incorrecto de coutinho
            elif token == 'coutinho':
                self.errors.encolar_error(
                    f"Error: falta paréntesis o punto y coma después de 'coutinho' en fila {row}, col {col}."
                )

            # 8. Identificadores inesperados
            elif token.isidentifier():
                self.errors.encolar_error(
                    f"Error: identificador inesperado '{token}' en fila {row}, col {col}. "
                    f"¿Falta un ';' en la línea anterior o se cerró mal un bloque?"
                )

            # 9. Números fuera de contexto
            elif p.type == 'NUMBER':
                self.errors.encolar_error(
                    f"Error: número inesperado '{p.value}' en fila {row}, col {col}. "
                    f"¿Se esperaba un operador antes?"
                )

            # 10. Fallback
            else:
                self.errors.encolar_error(
                    f"Error de sintaxis en '{token}' en fila {row}, col {col}."
                )

        except Exception as e:
            self.errors.encolar_error("Error interno analizando token inesperado: " + str(e))

    else:
        self.errors.encolar_error(
            "Error de sintaxis: final inesperado del archivo. "
            "¿Falta cerrar una llave '}' o completar una instrucción?"
        )
