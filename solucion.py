import json
import os
from tabulate import tabulate

def validar_reporte(token, horas):
    """Regla de decisión con 4 resultados evaluando 2 datos."""
    if horas < 0:
        return "Inválido", "Error: Las horas no pueden ser negativas"
    elif token != "PROFE123":
        return "Rechazado", "Token de acceso incorrecto"
    elif token == "PROFE123" and horas == 0:
        return "Rechazado", "Sin carga asignada este mes"
    else:
        return "Aceptado", "Acceso concedido al reporte"

# Este bloque solo se ejecuta al usar la consola, no cuando Django lo importe
if __name__ == "__main__":
    nombre = input("Nombre: ")
    token = input("Token: ")
    horas = int(input("Horas: "))
    
    # Evaluar regla
    estado, motivo = validar_reporte(token, horas)
    
    # Preparar el guardado
    registro = {
        "nombre": nombre,
        "estado": estado,
        "motivo": motivo
    }
    
    registros = []
    # Leer JSON si existe
    if os.path.exists("datos.json"):
        with open("datos.json", "r") as f:
            registros = json.load(f)
            
    registros.append(registro)
    
    # Guardar en JSON
    with open("datos.json", "w") as f:
        json.dump(registros, f, indent=2)
        
    # Mostrar tabla
    print(tabulate(registros, headers="keys"))
