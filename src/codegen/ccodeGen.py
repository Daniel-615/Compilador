class ccodeGen:
    def __init__(self, ir, symbol_table=None):
        self.ir = ir
        self.symbol_table = symbol_table or {}
        self.cpp_code = []
        self.indent_level = 0
        self.temp_conditions = {}  # Almacena tX = condicion
        self.label_to_index = {
            line.strip()[:-1]: idx
            for idx, line in enumerate(self.ir)
            if line.strip().endswith(":")
        }

    def indent(self):
        return "    " * self.indent_level

    def generate(self):
        declared = set()
        used_vars = set()
        open_blocks = []

        # Detectar variables usadas
        for line in self.ir:
            tokens = line.replace(';', '').replace('(', ' ').replace(')', ' ').split()
            for tok in tokens:
                if tok.isidentifier():
                    used_vars.add(tok)

        # Detectar variables declaradas y guardar condiciones temporales
        filtered_ir = []
        for line in self.ir:
            line = line.strip()
            if '=' in line and not line.startswith(("if", "goto")) and not line.endswith(":"):
                left, right = map(str.strip, line.split('=', 1))
                declared.add(left)
                if left.startswith('t') and left[1:].isdigit() and any(op in right for op in ['<', '>', '==', '!=', '<=', '>=']):
                    self.temp_conditions[left] = right
                    continue  # No agregues esta línea al código final
            filtered_ir.append(line)

        # Cabecera
        self.cpp_code = [
            "#include <iostream>",
            "#include <string>",
            "using namespace std;",
            "int main() {"
        ]

        # Declarar variables (excluyendo temporales)
        for var in sorted(declared):
            if var.startswith('t') and var[1:].isdigit():
                continue
            if var not in used_vars:
                continue
            tipo = self.symbol_table.get(var, {}).get("type", "auto")

            if tipo == "milito":
                tipo = "int"
            elif tipo == "zidane":
                tipo = "float"
            elif tipo == "saviola":
                tipo = "char"
            elif tipo == "valderrama":
                tipo = "bool"
            elif tipo == "iniesta":
                tipo = "string"

            self.cpp_code.append(f"    {tipo} {var};")

        # ✅ Declarar condiciones temporales tX = expresión
        for tvar, expr in sorted(self.temp_conditions.items()):
            self.cpp_code.append(f"    bool {tvar} = {self._translate_expression(expr)};")

        # Cuerpo del programa
        self.indent_level = 1
        for i, line in enumerate(filtered_ir):
            line = line.strip()
            if line.endswith(":"):
                continue
            elif line.startswith("if !("):
                condition = line[5:].split(') goto')[0].strip()
                condition_real = self.temp_conditions.get(condition, condition)
                target = line.split('goto')[1].strip()
                block_type = "if" if self.label_to_index.get(target, 0) > i else "while"
                self.cpp_code.append(f"{self.indent()}// INICIO {block_type.upper()};")
                self.cpp_code.append(f"{self.indent()}{block_type} (!({condition_real})) {{")
                self.indent_level += 1
                open_blocks.append(block_type)
            elif line.startswith("if"):
                condition = line[3:].split('goto')[0].strip()
                condition_real = self.temp_conditions.get(condition, condition)
                target = line.split('goto')[1].strip()
                block_type = "if" if self.label_to_index.get(target, 0) > i else "while"
                self.cpp_code.append(f"{self.indent()}// INICIO {block_type.upper()};")
                self.cpp_code.append(f"{self.indent()}{block_type} ({condition_real}) {{")
                self.indent_level += 1
                open_blocks.append(block_type)
            elif line.startswith("goto"):
                if open_blocks:
                    block = open_blocks.pop()
                    self.indent_level -= 1
                    self.cpp_code.append(f"{self.indent()}}} // FIN {block}")
            else:
                expr = self._translate_expression(line)
                if expr != "end":
                    self.cpp_code.append(f"{self.indent()}{expr};")

        while open_blocks:
            block = open_blocks.pop()
            self.indent_level -= 1
            self.cpp_code.append(f"{self.indent()}}} // FIN {block}")

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
            tipo_simbolo = self.symbol_table.get(left, {}).get("type", "")

            if tipo_simbolo == "saviola":
                right = f"'{right}'" if not (right.startswith("'") and right.endswith("'")) else right
            elif tipo_simbolo == "iniesta":
                right = f'"{right}"' if not (right.startswith('"') and right.endswith('"')) else right
            elif tipo_simbolo == "valderrama" and right.lower() in ["true", "false"]:
                right = right.lower()

            if right.startswith("call"):
                return f"{left} = {right.replace('call', '').strip()}()"

            return f"{left} = {right}"

        if line.startswith("call "):
            return f"{line.replace('call ', '').strip()}()"

        return line

    def get_cpp_code(self):
        return "\n".join(self.cpp_code)
