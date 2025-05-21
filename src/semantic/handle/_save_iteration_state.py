import json, os, tempfile
from datetime import datetime

def _save_iteration_state(self):
    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, "tabla_simbolos_iteracion_historial.json")

    # Cargar historial anterior si existe
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = []

    # Serializar variables globales
    global_serializado = {
        str(k): v["value"] for k, v in self.symbol_table.global_scope.items()
    }

    # Serializar scopes locales
    local_serializado = []
    for scope in self.symbol_table.scope_stack:
        scope_dict = {}
        for k, v in scope.items():
            scope_dict[str(k)] = {
                "type": v["type"],
                "scope": v["scope"],
                "value": v["value"]
            }
        local_serializado.append(scope_dict)

    # Guardar entrada en historial
    historial.append({
        "timestamp": datetime.now().isoformat(),
        "iteration": len(historial) + 1,
        "tabla": {
            "global": global_serializado,
            "local_scopes": local_serializado
        }
    })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4)
