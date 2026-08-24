import json, os
from django.shortcuts import render
# Importamos la regla de decisión desde tu archivo de consola (Bloque 11)
from solucion import validar_reporte

def resumen(request):
    archivo = "datos.json"
    registros = []

    # 1. Si el usuario envía el formulario web
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        token = request.POST.get("token")
        horas = int(request.POST.get("horas", 0))

        # Reutilizamos la lógica sin reescribirla
        estado, motivo = validar_reporte(token, horas)

        nuevo_registro = {
            "nombre": nombre,
            "horas": horas,  
            "estado": estado,
            "motivo": motivo
        }

        # Leer archivo existente para no borrar lo anterior
        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                try:
                    registros = json.load(f)
                except json.JSONDecodeError:
                    registros = []
        
        # Agregar y guardar
        registros.append(nuevo_registro)
        with open(archivo, "w") as f:
            json.dump(registros, f, indent=2)

    # 2. Si solo entra a ver la página (GET)
    else:
        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                try:
                    registros = json.load(f)
                except json.JSONDecodeError:
                    registros = []

    return render(request, "resumen.html", {"registros": registros})