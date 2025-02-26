class Token:
    def __init__(self, type, value, line, column):
        """Initialize the Token class"""
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value}, line={self.line}, column={self.column})"