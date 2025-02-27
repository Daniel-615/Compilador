# Proyecto de Compiladores

## Descripción
Este proyecto es una implementación de un compilador para un lenguaje de programación personalizado. El objetivo es analizar, interpretar y ejecutar código escrito en este lenguaje.

## Características
- Análisis léxico
- Análisis sintáctico
- Generación de código intermedio
- Optimización de código
- Generación de código máquina

## Requisitos
- Python 3.x
- PLY (Python Lex-Yacc)

## Instalación
1. Clona el repositorio:
    ```bash
    git clone https://github.com/Daniel-615/Compilador
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd compiladores
    ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso
Para compilar un archivo fuente, ejecuta el siguiente comando:
```bash
python main.py
```

## Estructura del Proyecto
- `lexer.py`: Contiene el analizador léxico.
- `parser.py`: Contiene el analizador sintáctico.
- `symbolTable.py`: Generación de tabla de simbolos.
- `files.py`: Lectura de archivo txt.
- `ccodeGen.py`: Generación de código máquina.
- `tests/`: Directorio con pruebas unitarias.
- `errors.py`: Bitácora de errores

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

