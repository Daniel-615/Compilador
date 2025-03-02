import os
import webbrowser

class Errors:
    def __init__(self):
        self.error_log_path = os.path.join('utils', 'log.html')
        self.create_log_file()

    def create_log_file(self):
        # Crear el archivo de log si no existe
        if not os.path.exists(self.error_log_path):
            with open(self.error_log_path, 'w') as file:
                file.write("""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Bitácora de Errores</title>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        table { width: 100%; border-collapse: collapse; }
                        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                        th { background-color: #f4f4f4; }
                    </style>
                </head>
                <body>
                    <h1>Bitácora de Errores Léxicos y Sintácticos</h1>
                    <table>
                        <thead>
                            <tr>
                                <th>Tipo de Error</th>
                                <th>Descripción</th>
                                <th>Ubicación</th>
                            </tr>
                        </thead>
                        <tbody id="error-log">
                """)

    def log_error(self, error_type, message, location):
        log_entry = f"""
        <tr>
            <td>{error_type}</td>
            <td>{message}</td>
            <td>{location}</td>
        </tr>
        """
        
        with open(self.error_log_path, 'a') as file:
            file.write(log_entry)

    def display_errors(self):
        webbrowser.open('file://' + os.path.realpath(self.error_log_path))

# Ejemplo de uso
if __name__ == "__main__":
    error_handler = Errors()
    error_handler.log_error("Léxico", "Carácter inesperado", "línea 10, columna 5")
    error_handler.display_errors()