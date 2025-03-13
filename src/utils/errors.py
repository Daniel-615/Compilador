import os
import webbrowser

class Errors:
    def __init__(self):
        self.errors = []  # Lista de errores

    def encolar_error(self, error):
        self.errors.append(error)  # Agregar error a la lista

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