import subprocess
import os
import sys

class GenerateExe:
    def __init__(self, name: str, version: str, description: str, author: str, author_email: str):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.author_email = author_email

    def generate_exe(self, entry_point="main.py", templates_folder="templates"):
        print("Iniciando generación del .exe...")

        if sys.prefix == sys.base_prefix:
            print("❌ No estás usando un entorno virtual. Por favor actívalo antes de generar el .exe.")
            return
        else:
            print(f"✅ Entorno virtual detectado: {sys.prefix}")

        # Intentar importar PyInstaller
        try:
            import PyInstaller
        except ImportError:
            print("🔵 PyInstaller no encontrado en el entorno virtual. Instalando...")
            pip_executable = os.path.join(sys.prefix, 'Scripts', 'pip.exe')
            subprocess.run([pip_executable, "install", "pyinstaller"], check=True)

        # Ubicar pyinstaller.exe dentro del entorno
        pyinstaller_executable = os.path.join(sys.prefix, 'Scripts', 'pyinstaller.exe')

        if not os.path.exists(pyinstaller_executable):
            print("❌ pyinstaller.exe no encontrado. ¿Seguro que PyInstaller se instaló correctamente?")
            return

        # Corregir el separador de carpetas para --add-data
        if os.name == 'nt':
            add_data = f"{templates_folder};{templates_folder}"
        else:
            add_data = f"{templates_folder}:{templates_folder}"

        # Comando final
        command = [
            pyinstaller_executable,
            "--onefile",
            "--noconsole",
            f"--name={self.name}",
            f"--add-data={add_data}",
            entry_point
        ]

        print(f"⚙️ Ejecutando: {' '.join(command)}")
        try:
            subprocess.run(command, check=True)
            print(f"✅ ¡{self.name}.exe generado exitosamente en la carpeta 'dist/'!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al generar el .exe: {e}")
