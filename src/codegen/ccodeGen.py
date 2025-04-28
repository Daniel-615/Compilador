class ccodeGen:
    def __init__(self, ir):
        self.ir = ir  # Código intermedio optimizado
        self.cpp_code = []
        self.label_to_index = {line.strip()[:-1]: idx for idx, line in enumerate(self.ir) if line.strip().endswith(":")}
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def generate(self):
        i = 0
        while i < len(self.ir):
            line = self.ir[i].strip()

            if line.endswith(":"):
                pass  # No escribir etiquetas

            elif line.startswith("if !("):
                condition = line[5:].split(') goto')[0]
                target_label = line.split('goto')[1].strip()

                # Decidir si es IF o WHILE (salto hacia adelante o hacia atrás)
                if self.label_to_index.get(target_label, 0) > i:
                    # Salto hacia adelante → es un IF
                    self.cpp_code.append(f"{self.indent()}if ({condition}) {{")
                    self.indent_level += 1
                else:
                    # Salto hacia atrás → es un WHILE
                    self.cpp_code.append(f"{self.indent()}while ({condition}) {{")
                    self.indent_level += 1

            elif line.startswith("if"):
                condition = line[3:].split('goto')[0].strip()
                target_label = line.split('goto')[1].strip()

                if self.label_to_index.get(target_label, 0) > i:
                    # Es un IF normal
                    self.cpp_code.append(f"{self.indent()}if ({condition}) {{")
                    self.indent_level += 1
                else:
                    # Muy raro aquí, pero tratar como while
                    self.cpp_code.append(f"{self.indent()}while ({condition}) {{")
                    self.indent_level += 1

            elif line.startswith("goto"):
                target_label = line.split('goto')[1].strip()

                if self.label_to_index.get(target_label, 0) < i:
                    # Salto hacia atrás → cerrar WHILE
                    self.indent_level -= 1
                    self.cpp_code.append(f"{self.indent()}}} // fin while")
                else:
                    # Salto hacia adelante → cerrar IF
                    self.indent_level -= 1
                    self.cpp_code.append(f"{self.indent()}}} // fin if")

            else:
                # Asignación normal
                self.cpp_code.append(f"{self.indent()}{self._translate_expression(line)};")

            i += 1

        # Cerrar cualquier bloque abierto al final
        while self.indent_level > 0:
            self.indent_level -= 1
            self.cpp_code.append(f"{self.indent()}}}")

    def _translate_expression(self, line):
        # Traduce operadores personalizados
        if 'cristiano' in line:
            return line.replace('cristiano', '+')
        if 'tchouameni' in line:
            return line.replace('tchouameni', '-')
        if 'messi' in line:
            return line.replace('messi', '*')
        if 'pepe' in line:
            return line.replace('pepe', '/')
        return line

    def get_cpp_code(self):
        return "\n".join(self.cpp_code)
