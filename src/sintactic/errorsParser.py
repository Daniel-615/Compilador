def p_error(self, p):
    if p:
        try:
            col = self.errors.find_column(p)
            row = self.errors.find_line(p)
            token = p.value.lower() if isinstance(p.value, str) else str(p.value)

            # Bloques mal cerrados o mal abiertos
            if token == '}':
                self.errors.encolar_error(
                    f"Error de sintaxis en '}}' en la fila {row} y columna {col}. "
                    f"¿Se cerró un bloque sin haberse abierto correctamente?"
                )
            elif token == '{':
                self.errors.encolar_error(
                    f"Error de sintaxis en '{{' en la fila {row} y columna {col}. "
                    f"¿Está mal ubicado el inicio del bloque?"
                )

            # Paréntesis
            elif token == '(':
                self.errors.encolar_error(
                    f"Error de sintaxis en '(' en la fila {row} y columna {col}. "
                    f"¿Está cerrando correctamente con ')'? "
                )
            elif token == ')':
                self.errors.encolar_error(
                    f"Error de sintaxis en ')' en la fila {row} y columna {col}. "
                    f"¿Se abrió correctamente con '('?"
                )

            # Estructuras de control
            elif token == 'walker':
                self.errors.encolar_error(
                    f"Error de sintaxis en 'walker' en la fila {row} y columna {col}. "
                    f"¿Falta el bloque '{{}}' o la condición está mal formada?"
                )
            elif token == 'ballack':
                self.errors.encolar_error(
                    f"Error de sintaxis en 'ballack' en la fila {row} y columna {col}. "
                    f"¿Falta el bloque '{{}}' que contiene el cuerpo del if?"
                )
            elif token == 'robben':
                self.errors.encolar_error(
                    f"Error de sintaxis en 'robben' en la fila {row} y columna {col}. "
                    f"¿El bloque 'if' anterior está cerrado correctamente con '}}'?"
                )
            elif token == 'ramos':
                self.errors.encolar_error(
                    f"Error de sintaxis en 'ramos' en la fila {row} y columna {col}. "
                    f"¿La sintaxis del for está completa? Verifica los ';' y el cuerpo con '{{}}'."
                )
            elif token == 'aguero':
                self.errors.encolar_error(
                    f"Error de sintaxis en 'aguero' en la fila {row} y columna {col}. "
                    f"¿Falta abrir el bloque del do-while con '{{'? "
                )
            elif token == 'forlan':
                self.errors.encolar_error(
                    f"Error de sintaxis en 'forlan' en la fila {row} y columna {col}. "
                    f"¿Falta el bloque '{{}}' para los casos del switch?"
                )
            elif token in {'son', 'ronaldinho'}:
                self.errors.encolar_error(
                    f"Error de sintaxis en '{p.value}' en la fila {row} y columna {col}. "
                    f"¿Estás dentro de un switch con '{{}}'? Verifica la apertura correcta del bloque."
                )

            # Operadores mal usados (condición mal formada)
            elif p.type == 'NUMBER':
                self.errors.encolar_error(
                    f"Error de sintaxis: número '{p.value}' inesperado en la fila {row} y columna {col}. "
                    f"¿Falta un operador relacional antes del número?"
                )

            # Literales mal cerrados
            elif token.startswith('"') or token.startswith("'"):
                self.errors.encolar_error(
                    f"Error: literal mal cerrado en la fila {row} y columna {col}."
                )

            # Operadores sin operandos
            elif token in {'cristiano', 'tchouameni', 'messi', 'pepe'}:
                self.errors.encolar_error(
                    f"Error de sintaxis: operador '{token}' usado incorrectamente o sin operandos en la fila {row} y columna {col}."
                )

            # Tipos sin identificador
            elif token in {'milito', 'zidane', 'saviola', 'iniesta', 'valderrama'}:
                self.errors.encolar_error(
                    f"Error: falta identificador después del tipo '{token}' en la fila {row} y columna {col}."
                )

            # Mal uso de coutinho
            elif token == 'coutinho':
                self.errors.encolar_error(
                    f"Error de sintaxis en 'coutinho' en la fila {row} y columna {col}. "
                    f"¿Falta el paréntesis con la expresión a imprimir o el punto y coma final?"
                )

            # Identificadores mal colocados
            elif token.isidentifier():
                self.errors.encolar_error(
                    f"Error de sintaxis antes de '{p.value}' en la fila {row} y columna {col}. "
                    f"¿Falta un ';' al final de la instrucción anterior o el bloque anterior no está cerrado?"
                )

            # Fallback general
            else:
                self.errors.encolar_error(
                    f"Error de sintaxis en '{p.value}' en la fila {row} y columna {col}."
                )

        except Exception:
            self.errors.encolar_error("Error de sintaxis en token inesperado.")
    else:
        self.errors.encolar_error(
            "Error de sintaxis: expresión incompleta o final inesperado. "
            "¿Falta cerrar una llave '}' o completar una estructura?"
        )
