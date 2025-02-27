import os
import webbrowser

class symbolTable:
    def __init__(self):
        """Initialize the symbol table."""
        self.symbols = []

    def insert(self, name, symbol_type, scope, value=None):
        """Insert to the table all values expected."""
        self.symbols.append({
            'name': name,
            'type': symbol_type,
            'scope': scope,
            'value': value
        })

    def lookup(self, name):
        """Look up the symbol by name."""
        for symbol in self.symbols:
            if symbol['name'] == name:
                return symbol
        return None

    def toHtml(self):
        """Return the symbol table as HTML."""
        html = '<table border="1">'
        html += '<tr><th>Name</th><th>Type</th><th>Scope</th><th>Value</th></tr>'
        for symbol in self.symbols:
            html += '<tr>'
            html += '<td>' + symbol['name'] + '</td>'
            html += '<td>' + symbol['type'] + '</td>'
            html += '<td>' + symbol['scope'] + '</td>'
            html += '<td>' + str(symbol['value']) + '</td>'
            html += '</tr>'
        html += '</table>'
        
        os.makedirs('templates', exist_ok=True)
        
        #Join tempaltes and symbol table html
        file_path = os.path.join('templates', 'symbol_table.html')
        with open(file_path, 'w') as file:
            file.write(html)
        
        #Open the file in the browser
        webbrowser.open('file://' + os.path.realpath(file_path))
        
        return html
