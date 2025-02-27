from src.utils.files import Files as f
class main:
    def __init__(self):
        """
        Initializes a new instance of the class.
        """
        file = f("lenguaje.txt")
        content, lines =file.read_file()

        if content:
            print("File read successfully!")
            print(lines)
        else:
            print("Could not read the file.")
    def main(self):
        main()

# Entry point of the program
main=main()
