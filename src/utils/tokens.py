import os
import webbrowser
class Tokens:
    def __init__(self):
        pass
    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
    def toHtml(self,tokens):
        """Genera un HTML con la lista de tokens generados por el lexer."""
        if not tokens:
            return "No hay tokens."

        html = f'<html><head><title>Tokens</title><link rel="stylesheet" href="./css/styles.css"</head><body>'
        html += f'<h2 style="color: red;">Tokens leídos</h2>'
        html += '<table border="1" style="width: 80%; margin: auto; text-align: left;">'
        html += '<tr><th>#</th><th>Descripción del Token</th></tr>'

        for i, tokens in enumerate(tokens, start=1):
            html += f'<tr><td>{i}</td><td>{tokens}</td></tr>'

        html += '</table></body></html>'

        # Guardar archivo
        os.makedirs('templates', exist_ok=True)
        file_path = os.path.join('templates', f'tokens.html')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html)

        webbrowser.open('file://' + os.path.realpath(file_path)) 

        return html