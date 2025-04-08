import os
import webbrowser

class SymbolTable:
    def __init__(self):
        # Diccionario para almacenar los símbolos (identificadores y sus valores)
        self.symbols = {}

    def add_symbol(self, name, type_, scope, value=None):
        if name in self.symbols:
            print(f"Error: Variable '{name}' ya está declarada en el alcance '{self.symbols[name]['scope']}'.")
        else:
            self.symbols[name] = {'type': type_, 'scope': scope, 'value': value}
            print(f"Variable '{name}' añadida con tipo '{type_}', alcance '{scope}' y valor '{value}'")

    def update_symbol(self, identifier, value):
        """Actualiza el valor de un símbolo existente en la tabla."""
        if identifier in self.symbols:
            self.symbols[identifier]['value'] = value
        else:
            print(f"Error: La variable '{identifier}' no ha sido declarada.")

    def get_symbol(self, identifier):
        """Obtiene el valor de una variable si existe en la tabla."""
        if identifier in self.symbols:
            return self.symbols[identifier]['value']
        else:
            print(f"Error: La variable '{identifier}' no ha sido declarada.")
            return None

    def exists(self, name, scope="local"):
        return (name, scope) in self.symbols
    
    def get_value(self, name, scope="local"):
        return self.symbols.get((name, scope), {}).get("value")
    
    def set_value(self, name, value, scope="local"):
        if (name, scope) in self.symbols:
            self.symbols[(name, scope)]["value"] = value

    def show_table(self):
        """Imprime la tabla de símbolos actual."""
        print("\nTabla de Símbolos:")
        for identifier, data in self.symbols.items():
            print(f"{identifier}: Tipo={data['type']}, Alcance={data['scope']}, Valor={data['value']}")

    def toHtml(self):
        """Retorna la tabla de símbolos como HTML."""
        html = '<html><head><title>Tabla de Símbolos</title><link rel="stylesheet" href="./css/styles.css"></head><body>'
        html += '<table border="1">'
        html += '<tr><th>Name</th><th>Type</th><th>Scope</th><th>Value</th></tr>'
        
        # Generar las filas de la tabla con la información de los símbolos
        for identifier, data in self.symbols.items():
            html += '<tr>'
            html += f'<td>{identifier}</td>'
            html += f'<td>{data["type"]}</td>'
            html += f'<td>{data["scope"]}</td>'
            html += f'<td>{str(data["value"])}</td>'  # Asegúrate de convertir a string el valor
            html += '</tr>'
        
        html += '</table>'
        
        # Crear el directorio 'templates' si no existe
        os.makedirs('templates', exist_ok=True)
        
        # Unir la plantilla y la tabla de símbolos HTML
        file_path = os.path.join('templates', 'symbol_table.html')
        with open(file_path, 'w') as file:
            file.write(html)
        
        # Abrir el archivo en el navegador
        webbrowser.open('file://' + os.path.realpath(file_path))
        
        return html