def p_error(self, p):
        if p:
            try:
                col = self.errors.find_column(p)
                row = self.errors.find_line(p)
                token = p.value.lower() if isinstance(p.value, str) else str(p.value)

                # Errores comunes relacionados con estructuras de control y delimitadores
                if token in {'}', 'walker', 'ballack', 'robben', 'ramos', 'forlan', 'aguero', 'son', 'ronaldinho'}:
                    self.errors.encolar_error(
                        f"Error de sintaxis antes de '{p.value}' en la fila {row} y columna {col}. "
                        f"¿Falta un ';' al final de la instrucción anterior o el bloque anterior no está cerrado?"
                    )

                elif token == '}':
                    self.errors.encolar_error(
                        f"Error de sintaxis en '}}' en la fila {row} y columna {col}. "
                        f"¿Se cerró un bloque sin haberse abierto correctamente?"
                    )
                elif token == '{':
                    self.errors.encolar_error(
                        f"Error de sintaxis en '{{' en la fila {row} y columna {col}. "
                        f"¿Está mal ubicado el inicio del bloque?"
                    )
                elif token == '(':
                    self.errors.encolar_error(
                        f"Error de sintaxis en '(' en la fila {row} y columna {col}. "
                        f"¿Está cerrando correctamente con ')'?"
                        )
                elif token == ')':
                    self.errors.encolar_error(
                        f"Error de sintaxis en ')' en la fila {row} y columna {col}. "
                        f"¿Se abrió correctamente con '('?"
                    )
                elif token == 'robben':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'robben' en la fila {row} y columna {col}. "
                        f"¿El bloque 'if' anterior está cerrado correctamente con '}}'?"
                    )
                elif token == 'walker':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'walker' en la fila {row} y columna {col}. "
                        f"¿Falta el bloque '{{}}' que contiene el cuerpo del ciclo?"
                    )
                elif token == 'ballack':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'ballack' en la fila {row} y columna {col}. "
                        f"¿Falta el bloque '{{}}' que contiene el cuerpo del if?"
                    )

                # Errores comunes semánticos o de estilo
                elif token == 'coutinho':
                    self.errors.encolar_error(
                        f"Error de sintaxis en 'coutinho' en la fila {row} y columna {col}. "
                        f"¿Falta el paréntesis con la expresión a imprimir o el punto y coma final?"
                    )
                elif token.startswith('"') or token.startswith("'"):
                    self.errors.encolar_error(
                        f"Error: literal mal cerrado en la fila {row} y columna {col}."
                    )
                elif token.isdigit() and not p.type == 'NUMBER':
                    self.errors.encolar_error(
                        f"Error: identificador no válido '{p.value}' en la fila {row} y columna {col}. "
                        f"Los identificadores no pueden comenzar con números."
                    )
                elif token in {'cristiano', 'tchouameni', 'messi', 'pepe'}:
                    self.errors.encolar_error(
                        f"Error de sintaxis: operador '{token}' usado incorrectamente o sin operandos en la fila {row} y columna {col}."
                    )
                elif token in {'milito', 'zidane', 'saviola', 'iniesta', 'valderrama'}:
                    self.errors.encolar_error(
                        f"Error: falta identificador después del tipo '{token}' en la fila {row} y columna {col}."
                    )
                elif token.isidentifier():
                    self.errors.encolar_error(
                        f"Error de sintaxis en '{p.value}' en la fila {row} y columna {col}. "
                        f"¿Falta un ';' al final de la instrucción?"
                    )
                elif token.isidentifier():
                    self.errors.encolar_error(
                        f"Error de sintaxis antes de '{p.value}' en la fila {row} y columna {col}. "
                        f"¿Falta un ';' al final de la instrucción anterior o el bloque anterior no está cerrado?"
                    )
                else:
                    self.errors.encolar_error(
                        f"Error de sintaxis en '{p.value}' en la fila {row} y columna {col}."
                    )

            except Exception:
                self.errors.encolar_error("Error de sintaxis en token inesperado.")

        else:
            # Fin del archivo: probablemente falta una llave de cierre
            self.errors.encolar_error(
                "Error de sintaxis: expresión incompleta o final inesperado. ¿Falta cerrar una llave '}' de alguna estructura?"
            )