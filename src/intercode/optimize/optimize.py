class Optimize:
    def __init__(self, ir):
        self.ir = ir  # intermediate representation (lista de instrucciones)

    def remove_redundant_temporaries(self):
        """
        Fusión de temporales: convierte
        t0 = goles cristiano 5
        goles = t0
        → goles = goles cristiano 5
        """
        optimized_ir = []
        i = 0
        while i < len(self.ir):
            line = self.ir[i].strip()
            if i + 1 < len(self.ir):
                next_line = self.ir[i+1].strip()
                # Detectar patrón t0 = expr / var = t0
                if "=" in line and "=" in next_line:
                    left1, expr1 = line.split('=', 1)
                    left2, expr2 = next_line.split('=', 1)
                    if expr2.strip() == left1.strip():
                        # Fusión: reescribimos la segunda usando expr1
                        optimized_ir.append(f"{left2.strip()} = {expr1.strip()}")
                        i += 2
                        continue
            optimized_ir.append(line)
            i += 1
        self.ir = optimized_ir

    def simplify_trivial_operations(self):
        """
         Elimina operaciones triviales como + 0, - 0, * 1, / 1
        """
        optimized_ir = []
        for line in self.ir:
            if '+ 0' in line or '- 0' in line:
                left, expr = line.split('=', 1)
                var, op, num = expr.strip().split()
                if op in ['+', '-'] and num == '0':
                    optimized_ir.append(f"{left.strip()} = {var.strip()}")
                    continue
            if '* 1' in line or '/ 1' in line:
                left, expr = line.split('=', 1)
                var, op, num = expr.strip().split()
                if (op == '*' and num == '1') or (op == '/' and num == '1'):
                    optimized_ir.append(f"{left.strip()} = {var.strip()}")
                    continue
            optimized_ir.append(line)
        self.ir = optimized_ir

    def optimize_conditionals(self):
        """
         Mejora IFs: convierte
        if condition goto L1
        goto L2
        L1:
        ...
        → if !condition goto L2
        (reduce 1 salto innecesario)
        """
        optimized_ir = []
        i = 0
        while i < len(self.ir):
            if i + 2 < len(self.ir):
                line_if = self.ir[i].strip()
                line_goto = self.ir[i+1].strip()
                line_label = self.ir[i+2].strip()

                if line_if.startswith('if') and line_goto.startswith('goto') and line_label.endswith(':'):
                    # Mejorar condición
                    cond_part = line_if[2:].strip().split('goto')[0].strip()
                    false_label = line_goto.split('goto')[1].strip()
                    optimized_ir.append(f"if !({cond_part}) goto {false_label}")
                    i += 2  # saltamos el if y el goto
                    continue
            optimized_ir.append(self.ir[i])
            i += 1
        self.ir = optimized_ir

    def remove_unreachable_labels(self):
        """
         Elimina labels innecesarias (cuando están pegadas después de GOTO)
        """
        optimized_ir = []
        last_was_goto = False
        for line in self.ir:
            if last_was_goto and line.endswith(':'):
                # No agregamos etiqueta no usada
                continue
            optimized_ir.append(line)
            last_was_goto = line.strip().startswith('goto')
        self.ir = optimized_ir
    def optimize_goto_chains(self):
        """
        Optimiza saltos innecesarios en cadena.
        Ejemplo:
        goto L1
        L1:
        goto L2
        -->
        goto L2
        """
        label_to_target = {}
        # Primero: construir a qué label apunta cada label
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

    def optimize(self):
        """
        Método principal para ejecutar todas las optimizaciones.
        """
        print(" Iniciando optimización...")
        self.remove_redundant_temporaries()
        self.simplify_trivial_operations()
        self.optimize_conditionals()
        self.remove_unreachable_labels()
        self.optimize_goto_chains() 
        print("Optimización completada.")

    def get_optimized_ir(self):
        """
        Devuelve la lista de instrucciones optimizadas.
        """
        return self.ir
