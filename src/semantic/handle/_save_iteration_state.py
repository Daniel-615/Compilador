import json, os, tempfile
from datetime import datetime
def _save_iteration_state(self):
        temp_dir = tempfile.gettempdir()
        path = os.path.join(temp_dir, "tabla_simbolos_iteracion_historial.json")

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                historial = json.load(f)
        else:
            historial = []

        historial.append({
            "timestamp": datetime.now().isoformat(),
            "iteration": len(historial) + 1,
            "tabla": self.symbol_table.symbols
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4)
