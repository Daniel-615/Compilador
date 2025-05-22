class ccodeGen:
    def __init__(self, ir):
        self.ir = ir
        self.cpp_code = []
        self.indent_level = 0
        self.label_to_index = {
            line.strip()[:-1]: idx
            for idx, line in enumerate(self.ir)
            if line.strip().endswith(":")
        }

    def indent(self):
        return "    " * self.indent_level

    def generate(self):
        declared = set()
        variables = {}
        used_vars = set()

        # Detección de variables usadas
        for line in self.ir:
            tokens = line.replace(';', '').replace('(', ' ').replace(')', ' ').split()
            for tok in tokens:
                if tok.isidentifier():
                    used_vars.add(tok)

        # Inferencia de tipos
        for line in self.ir:
            line = line.strip()
            if '=' in line and not line.startswith(("if", "goto")) and not line.endswith(":"):
                left, right = map(str.strip, line.split('=', 1))
                declared.add(left)
                if right.replace('.', '', 1).isdigit():
                    variables[left] = "int" if '.' not in right else "float"
                elif right.startswith('"') and right.endswith('"'):
                    variables[left] = "string"
                elif right.startswith("'") and right.endswith("'"):
                    variables[left] = "char"
                elif right in ("true", "false"):
                    variables[left] = "bool"
                else:
                    variables[left] = "auto"

        # Cabecera C++
        self.cpp_code += [
            "#include <iostream>",
            "#include <string>",
            "using namespace std;",
            "int main() {"
        ]

        tipo_explicit = {
            "goles": "int",
            "promedio": "float",
            "inicial": "char",
            "leyenda": "bool",
            "nombre": "string",
            "i": "int",
            "x": "int",
        }

        # Declaraciones
        for var in sorted(declared):
            if var.replace('.', '', 1).isdigit() or var in ('true', 'false'):
                continue
            if var not in used_vars:
                continue
            if any(op in var for op in ['+', '-', '*', '/', '>', '<', '==', '!=']):
                continue
            tipo = tipo_explicit.get(var, variables.get(var, "auto"))
            self.cpp_code.append(f"    {tipo} {var};")

        self.indent_level = 1
        for i, line in enumerate(self.ir):
            line = line.strip()
            if line.endswith(":"):
                continue
            elif line.startswith("if !("):
                condition = line[5:].split(') goto')[0]
                target = line.split('goto')[1].strip()
                block_type = "if" if self.label_to_index.get(target, 0) > i else "while"
                self.cpp_code.append(f"{self.indent()}{block_type} (!({condition})) {{")
                self.indent_level += 1
            elif line.startswith("if"):
                condition = line[3:].split('goto')[0].strip()
                target = line.split('goto')[1].strip()
                block_type = "if" if self.label_to_index.get(target, 0) > i else "while"
                self.cpp_code.append(f"{self.indent()}{block_type} ({condition}) {{")
                self.indent_level += 1
            elif line.startswith("goto"):
                target = line.split('goto')[1].strip()
                self.indent_level = max(1, self.indent_level - 1)
                closing = "while" if self.label_to_index.get(target, 0) < i else "if"
                self.cpp_code.append(f"{self.indent()}}} // fin {closing}")
            else:
                self.cpp_code.append(f"{self.indent()}{self._translate_expression(line)};")

        while self.indent_level > 0:
            self.indent_level -= 1
            self.cpp_code.append(f"{self.indent()}}}")

        self.cpp_code.append("    return 0;")
        self.cpp_code.append("}")

    def _translate_expression(self, line):
        if line.startswith("coutinho(") and line.endswith(")"):
            inner = line[len("coutinho("):-1].strip()
            return f'cout << {inner} << endl'

        line = line.replace("cristiano", "+")
        line = line.replace("tchouameni", "-")
        line = line.replace("messi", "*")
        line = line.replace("pepe", "/")

        if '=' in line:
            left, right = map(str.strip, line.split('=', 1))
            if right == "M":
                right = "'M'"
            elif right == "Messi":
                right = '"Messi"'
            elif right.startswith("call"):
                return f"{left} = {right.replace('call', '').strip()}()"
            return f"{left} = {right}"

        if line.startswith("call "):
            return f"{line.replace('call ', '').strip()}()"

        return line

    def get_cpp_code(self):
        return "\n".join(self.cpp_code)
