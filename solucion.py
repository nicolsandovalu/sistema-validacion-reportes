import json
import os
from tabulate import tabulate

# Simulamos la "base de datos" de RRHH con un diccionario
TOKENS_AUTORIZADOS = {
    "N2611": "Nicol Sandoval",
    "J2026": "Juan Pablo Díaz",
    "A1000": "Profesor Invitado"
}

def validar_reporte(token, horas):
    """Regla de decisión con 4 resultados evaluando 2 datos."""
    # 1. Dato Inválido
    if horas < 0:
        return "Inválido", "Error: Las horas no pueden ser negativas"
    
    # 2. Rechazo 1: El token no existe en nuestro diccionario
    elif token not in TOKENS_AUTORIZADOS:
        return "Rechazado", "Token de acceso incorrecto o no registrado"
    
    # 3. Rechazo 2: El token existe, pero el profesor no tiene horas
    elif token in TOKENS_AUTORIZADOS and horas == 0:
        nombre_profe = TOKENS_AUTORIZADOS[token]
        return "Rechazado", f"Sin carga asignada este mes para {nombre_profe}"
    
    # 4. Aceptado
    else:
        nombre_profe = TOKENS_AUTORIZADOS[token]
        return "Aceptado", f"Acceso concedido al reporte de {nombre_profe}"

# Bloque para probar desde la terminal
if __name__ == "__main__":
    nombre = input("Nombre de quien consulta: ")
    token = input("Token: ")
    horas = int(input("Horas: "))
    
    estado, motivo = validar_reporte(token, horas)
    
    registro = {
        "nombre": nombre,
        "horas": horas,  # <-- ¡Agregamos esta línea!
        "estado": estado,
        "motivo": motivo
    }
    
    registros = []
    if os.path.exists("datos.json"):
        with open("datos.json", "r") as f:
            registros = json.load(f)
            
    registros.append(registro)
    
    with open("datos.json", "w") as f:
        json.dump(registros, f, indent=2)
        
    print(tabulate(registros, headers="keys"))