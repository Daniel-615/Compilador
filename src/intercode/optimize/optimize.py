class Optimize:
    def __init__(self, ir):
        self.ir = ir  # Lista de instrucciones en código intermedio

    def remove_redundant_temporaries(self):
        """
        Elimina temporales innecesarios:
        Ejemplo:
            t1 = goles + 5
            goles = t1
        Se convierte en:
            goles = goles + 5
        """
        optimized_ir = []
        i = 0
        while i < len(self.ir):
            line = self.ir[i].strip()
            if i + 1 < len(self.ir):
                next_line = self.ir[i + 1].strip()
                if "=" in line and "=" in next_line:
                    left1, expr1 = line.split("=", 1)
                    left2, expr2 = next_line.split("=", 1)
                    if expr2.strip() == left1.strip():
                        optimized_ir.append(f"{left2.strip()} = {expr1.strip()}")
                        i += 2
                        continue
            optimized_ir.append(line)
            i += 1
        self.ir = optimized_ir

    def simplify_trivial_operations(self):
        """
        Elimina operaciones triviales como:
            t = x + 0 → t = x
            t = x * 1 → t = x
        """
        optimized_ir = []
        for line in self.ir:
            if '+ 0' in line or '- 0' in line:
                left, expr = line.split('=', 1)
                var, op, num = expr.strip().split()
                if num == '0':
                    optimized_ir.append(f"{left.strip()} = {var.strip()}")
                    continue
            if '* 1' in line or '/ 1' in line:
                left, expr = line.split('=', 1)
                var, op, num = expr.strip().split()
                if num == '1':
                    optimized_ir.append(f"{left.strip()} = {var.strip()}")
                    continue
            optimized_ir.append(line)
        self.ir = optimized_ir

    def optimize_conditionals(self):
        """
        Simplifica estructuras if + goto:
            if cond goto L1
            goto L2
            L1:
        Se convierte en:
            if !(cond) goto L2
        """
        optimized_ir = []
        i = 0
        while i < len(self.ir):
            if i + 2 < len(self.ir):
                line_if = self.ir[i].strip()
                line_goto = self.ir[i + 1].strip()
                line_label = self.ir[i + 2].strip()

                if line_if.startswith('if') and line_goto.startswith('goto') and line_label.endswith(':'):
                    cond = line_if[2:].split('goto')[0].strip()
                    false_label = line_goto.split('goto')[1].strip()
                    optimized_ir.append(f"if !({cond}) goto {false_label}")
                    i += 2
                    continue
            optimized_ir.append(self.ir[i])
            i += 1
        self.ir = optimized_ir

    def remove_unreachable_labels(self):
        """
        Elimina etiquetas inmediatamente después de un goto (no son alcanzables).
        """
        optimized_ir = []
        last_was_goto = False
        for line in self.ir:
            if last_was_goto and line.endswith(':'):
                continue
            optimized_ir.append(line)
            last_was_goto = line.strip().startswith('goto')
        self.ir = optimized_ir

    def optimize_goto_chains(self):
        """
        Elimina cadenas de saltos:
            L1:
            goto L2
            ...
            goto L1 → se convierte en → goto L2
        """
        label_to_target = {}
        for i in range(len(self.ir) - 1):
            line = self.ir[i].strip()
            next_line = self.ir[i + 1].strip()
            if line.endswith(':') and next_line.startswith('goto'):
                label = line[:-1].strip()
                target = next_line.split('goto')[1].strip()
                label_to_target[label] = target

        optimized_ir = []
        for line in self.ir:
            if line.startswith('goto'):
                dest = line.split('goto')[1].strip()
                while dest in label_to_target:
                    dest = label_to_target[dest]
                optimized_ir.append(f"goto {dest}")
            else:
                optimized_ir.append(line)
        self.ir = optimized_ir

    def remove_unused_temporaries(self):
        """
        Elimina asignaciones a temporales que nunca se usan.
        """
        used = set()
        for line in self.ir:
            parts = line.replace(';', '').replace('(', ' ').replace(')', ' ').split()
            for part in parts[1:]:  # Ignorar el lado izquierdo
                if part.startswith('t') and part[1:].isdigit():
                    used.add(part)

        optimized_ir = []
        for line in self.ir:
            if '=' in line:
                left = line.split('=')[0].strip()
                if left.startswith('t') and left not in used:
                    continue
            optimized_ir.append(line)
        self.ir = optimized_ir

    def optimize(self):
        """
        Ejecuta todas las optimizaciones.
        """
        print("🔧 Iniciando optimización...")
        self.remove_redundant_temporaries()
        self.simplify_trivial_operations()
        self.optimize_conditionals()
        self.remove_unreachable_labels()
        self.optimize_goto_chains()
        self.remove_unused_temporaries()
        print("✅ Optimización completada.")

    def get_optimized_ir(self):
        return self.ir
