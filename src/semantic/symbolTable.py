import os
import webbrowser

class SymbolTable:
    def __init__(self):
        # Diccionario para almacenar los símbolos (identificadores y sus valores)
        self.symbols = {}

    def add_symbol(self, identifier, datatype):
        """Agrega un nuevo símbolo a la tabla con su tipo de dato."""
        if identifier in self.symbols:
            print(f"Error: La variable '{identifier}' ya ha sido declarada.")
        else:
            self.symbols[identifier] = {'type': datatype, 'value': None}

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

    def exists(self, identifier):
        """Verifica si un símbolo existe en la tabla."""
        return identifier in self.symbols

    def show_table(self):
        """Imprime la tabla de símbolos actual."""
        print("\nTabla de Símbolos:")
        for identifier, data in self.symbols.items():
            print(f"{identifier}: Tipo={data['type']}, Valor={data['value']}")

    def toHtml(self):
        """Return the symbol table as HTML."""
        html = '<html><head><title>Tabla de Símbolos</title><link rel="stylesheet" href="./css/styles.css"</head><body>'
        html += '<table border="1">'
        html += '<tr><th>Name</th><th>Type</th><th>Value</th></tr>'
        
        # Generar las filas de la tabla con la información de los símbolos
        for identifier, data in self.symbols.items():
            html += '<tr>'
            html += f'<td>{identifier}</td>'
            html += f'<td>{data["type"]}</td>'
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