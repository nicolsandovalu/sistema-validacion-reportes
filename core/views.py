import json, os
from django.shortcuts import render

def resumen(request):
    registros = []
    if os.path.exists("datos.json"):
        with open("datos.json") as f:
            registros = json.load(f)
            
    return render(request, "resumen.html", {"registros": registros})