import os
import webbrowser

class Errors:
    def __init__(self,content):
        self.errors = []  # Lista de errores
        self.text=content
    def getText(self):
        return self.text
    def encolar_error(self, error):
        self.errors.append(error)

    def find_line(self, token):
        """Encuentra la fila (número de línea) de un token en el texto de entrada"""
        # Contar el número de saltos de línea antes de la posición del token
        line_count = self.getText().count('\n', 0, token.lexpos)
        # La fila es igual al número de saltos de línea + 1
        return line_count + 1
    
    def find_column(self,  token):
        """Encuentra la columna de un token en el texto de entrada"""
        # Obtener la posición del último salto de línea antes de lexpos
        last_newline = self.getText().rfind('\n', 0, token.lexpos)
        # Si no encontramos salto de línea, significa que estamos en la primera línea
        if last_newline == -1:
            # Devuelve la columna como la posición del token + 1 (ajustando por 0-indexed)
            return token.lexpos + 1  
        
        # Si encontramos un salto de línea, la columna es la diferencia entre lexpos y el último salto de línea
        column = token.lexpos - last_newline
        
        return column


    def errorHtml(self, nombre_archivo):
        """Genera un HTML con la lista de errores sintácticos y léxicos en una tabla"""
        if not self.errors:
            return "No hay errores."

        html = f'<html><head><title>Errores {nombre_archivo}</title><link rel="stylesheet" href="./css/styles.css"</head><body>'
        html += f'<h2 style="color: red;">Errores {nombre_archivo}</h2>'
        html += '<table border="1" style="width: 80%; margin: auto; text-align: left;">'
        html += '<tr><th>#</th><th>Descripción del Error</th></tr>'

        for i, error in enumerate(self.errors, start=1):
            html += f'<tr><td>{i}</td><td>{error}</td></tr>'

        html += '</table></body></html>'

        # Guardar archivo
        os.makedirs('templates', exist_ok=True)
        file_path = os.path.join('templates', f'errors_{nombre_archivo}.html')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html)

        webbrowser.open('file://' + os.path.realpath(file_path))  # Abrir en navegador

        return html