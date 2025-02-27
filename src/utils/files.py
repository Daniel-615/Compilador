import os

class Files:
    def __init__(self, path):
        self.path = path

    def read_file(self):
        """Reads the file from the given path and handles errors properly."""
        if not os.path.exists(self.path):
            print(f"Error: The file '{self.path}' was not found.")
            return None, None
        
        try:
            with open(self.path, 'r', encoding="utf-8") as file:
                content = file.read()
                lines = content.splitlines()
                return content, lines
        except PermissionError:
            print(f"Error: Permission denied to read '{self.path}'.")
        except Exception as e:
            print(f"An error occurred while reading '{self.path}': {e}")

        return None, None
