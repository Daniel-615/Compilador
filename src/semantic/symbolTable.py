import os
import webbrowser

class SymbolTable:
    def __init__(self):
        self.global_scope = {}       # Variables globales
        self.scope_stack = []        # Pila de ámbitos locales (de exterior a interior)

    def enter_scope(self):
        """Crea un nuevo ámbito local."""
        self.scope_stack.append({})
        print("🟢 Nuevo ámbito local creado.")

    def exit_scope(self):
        """Sale del ámbito local actual."""
        if self.scope_stack:
            self.scope_stack.pop()
            print("🔴 Ámbito local cerrado.")
        else:
            print("⚠️ Advertencia: No hay ningún ámbito local para salir.")

    def current_scope(self):
        """Retorna el ámbito local actual (el más interno)."""
        return self.scope_stack[-1] if self.scope_stack else None

    def add_symbol(self, name, type_, scope, value=None):
        """Agrega una nueva variable con su tipo, valor y alcance."""
        if scope == 'global':
            if name in self.global_scope:
                print(f"❌ Error: Variable global '{name}' ya declarada.")
            else:
                self.global_scope[name] = {'type': type_, 'scope': 'global', 'value': value}
                print(f"✅ [GLOBAL] Variable '{name}' añadida con valor '{value}'")
        elif scope == 'local':
            current = self.current_scope()
            if current is None:
                print(f"❌ Error: No hay un contexto local activo para declarar '{name}'.")
                return
            if name in current:
                print(f"❌ Error: Variable local '{name}' ya declarada en este ámbito.")
            else:
                current[name] = {'type': type_, 'scope': 'local', 'value': value}
                print(f"✅ [LOCAL] Variable '{name}' añadida con valor '{value}'")
        else:
            print(f"❌ Error: Alcance '{scope}' no reconocido para '{name}'.")

    def update_symbol(self, name, value):
        """Actualiza el valor de una variable existente en el ámbito correcto."""
        for scope in reversed(self.scope_stack):
            if name in scope:
                scope[name]['value'] = value
                print(f"🔄 Actualizado local '{name}' a {value}")
                return
        if name in self.global_scope:
            self.global_scope[name]['value'] = value
            print(f"🔄 Actualizado global '{name}' a {value}")
        else:
            print(f"❌ Error: La variable '{name}' no ha sido declarada.")

    def get_symbol(self, name):
        """Obtiene el valor de una variable desde el ámbito más interno hacia afuera."""
        for scope in reversed(self.scope_stack):
            if name in scope:
                val = scope[name]['value']
                print(f"📦 Valor local de '{name}': {val}")
                return val
        if name in self.global_scope:
            val = self.global_scope[name]['value']
            print(f"📦 Valor global de '{name}': {val}")
            return val
        print(f"❌ Error: La variable '{name}' no ha sido declarada.")
        return None

    def show_table(self):
        """Imprime la tabla de símbolos actual en consola."""
        print("\n📘 Tabla de Símbolos Globales:")
        for identifier, data in self.global_scope.items():
            print(f"  {identifier}: Tipo={data['type']}, Alcance={data['scope']}, Valor={data['value']}")

        print("\n📙 Ámbitos Locales (de exterior a interior):")
        for i, scope in enumerate(self.scope_stack):
            print(f"  Ámbito Local #{i + 1}:")
            for identifier, data in scope.items():
                print(f"    {identifier}: Tipo={data['type']}, Valor={data['value']}")

    def toHtml(self):
        """Genera una vista HTML de todos los símbolos."""
        html = '<html><head><title>Tabla de Símbolos</title><link rel="stylesheet" href="./css/styles.css"></head><body>'
        html += '<h1>Tabla de Símbolos</h1>'

        # Tabla global
        html += '<h2>Variables Globales</h2>'
        html += '<table border="1"><tr><th>Nombre</th><th>Tipo</th><th>Alcance</th><th>Valor</th></tr>'
        for identifier, data in self.global_scope.items():
            html += f"<tr><td>{identifier}</td><td>{data['type']}</td><td>global</td><td>{str(data['value'])}</td></tr>"
        html += '</table>'

        # Tabla de ámbitos locales
        html += '<h2>Variables Locales</h2>'
        for idx, scope in enumerate(self.scope_stack):
            html += f'<h3>Ámbito Local #{idx + 1}</h3>'
            html += '<table border="1"><tr><th>Nombre</th><th>Tipo</th><th>Alcance</th><th>Valor</th></tr>'
            for identifier, data in scope.items():
                html += f"<tr><td>{identifier}</td><td>{data['type']}</td><td>local</td><td>{str(data['value'])}</td></tr>"
            html += '</table>'

        html += '</body></html>'

        os.makedirs('templates', exist_ok=True)
        file_path = os.path.join('templates', 'symbol_table.html')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html)

        return html
