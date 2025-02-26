class symbolTable:
    def __init__(self):
        """Initialize the symbol table."""
        self.symbols=[]
    def insert(self,name,symbol_type,scope,value=None):
        """Insert to the table all values expected."""
        self.symbols.append({
            'name':name,
            'type':symbol_type,
            'scope':scope,
            'value':value
            })
    def lookup(self,name):
        """Look up the symbol by name."""
        for symbol in self.symbols:
            if symbol['name']==name:
                return symbol
        return None