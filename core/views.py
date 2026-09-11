import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profesor, Registro
from .decorators import requiere_rol

@requiere_rol("admin", "normal")
def gestion_tokens(request):
    # --- 1. PROCESAMIENTO DEL CSV ---
    if request.method == "POST" and request.FILES.get('archivo_csv'):
        datos_crudos = request.FILES['archivo_csv'].read()
        try:
            archivo = datos_crudos.decode('utf-8-sig').splitlines()
        except UnicodeDecodeError:
            archivo = datos_crudos.decode('latin-1').splitlines()
            
        lector = csv.DictReader(archivo, delimiter=',') 
        nuevos_creados = 0
        
        for fila in lector:
            nombre_limpio = fila.get('Profesor', '').strip()
            correo = fila.get('Correo', '').strip()
            
            if nombre_limpio and correo:
                profesor, creado = Profesor.objects.get_or_create(
                    nombre=nombre_limpio, defaults={'correo': correo}
                )
                if creado:
                    nuevos_creados += 1
                    send_mail(
                        subject='Bienvenido: Su Token de Acceso Académico',
                        message=f'Estimado/a {profesor.nombre},\n\nSu token único de acceso es: {profesor.token}',
                        from_email='coordinacion@institucion.cl',
                        recipient_list=[profesor.correo],
                        fail_silently=True, 
                    )
        
        if nuevos_creados > 0:
            messages.success(request, f"¡Éxito! Se registraron {nuevos_creados} profesores y se enviaron sus tokens.")
        else:
            messages.info(request, "No se generaron tokens nuevos (ya existían o el CSV tiene formato incorrecto).")
        return redirect('gestion_tokens')

    # --- 2. CARGA DEL DASHBOARD Y FILTROS ---
    profesores = Profesor.objects.all().order_by('-id')
    nombre_filtro = request.GET.get('nombre', '').strip()
    
    if nombre_filtro:
        profesores = profesores.filter(nombre__icontains=nombre_filtro)
        
    return render(request, "gestion_tokens.html", {
        "profesores": profesores,
        "nombre_filtro": nombre_filtro
    })


@requiere_rol("admin", "normal")
def gestion_reportes(request):
    # --- 1. PROCESAMIENTO DEL CSV ---
    if request.method == "POST" and request.FILES.get('archivo_csv'):
        datos_crudos = request.FILES['archivo_csv'].read()
        try:
            archivo = datos_crudos.decode('utf-8-sig').splitlines()
        except UnicodeDecodeError:
            archivo = datos_crudos.decode('latin-1').splitlines()
            
        lector = csv.DictReader(archivo, delimiter=',') 
        creados = 0
        errores = []
        
        for fila in lector:
            nombre_reporte = fila.get('Profesor', '').strip()
            profesor = Profesor.objects.filter(nombre__iexact=nombre_reporte).first()
            
            if not profesor:
                errores.append(nombre_reporte)
                continue
                
            cantidad = int(fila.get('Cantidad de Respuestas', 0))
            
            Registro.objects.create(
                profesor=profesor,
                programa=fila.get('Programa', '').strip(),
                cantidad=cantidad,
                estado=fila.get('Estado', '').strip(),
                pago_profesores=int(fila.get('Pago Profesores', 0)),
                ventas_totales=int(fila.get('Ventas Totales', 0)),
                cantidad_respuestas=cantidad,
                isn=int(fila.get('ISN', 0)),
                nps=int(fila.get('NPS', 0)),
                resultado="" # Lo dejamos vacío para no romper la base de datos
            )
            creados += 1
            
        if errores:
            nombres_unicos = set(errores)
            messages.warning(request, f"Se cargaron {creados} reportes. OMITIDOS por nombre inexacto: {', '.join(nombres_unicos)}")
        else:
            messages.success(request, f"¡Reportes vinculados correctamente! Se generaron {creados} informes.")
        return redirect('gestion_reportes')

    # --- 2. CARGA DEL DASHBOARD Y FILTROS ---
    reportes = Registro.objects.filter(eliminado=False).select_related('profesor').order_by('-fecha')
    profesor_filtro = request.GET.get('profesor', '').strip()
    programa_filtro = request.GET.get('programa', '').strip()
    estado_filtro = request.GET.get('estado', '').strip()

    if profesor_filtro:
        reportes = reportes.filter(profesor__nombre__icontains=profesor_filtro)
    if programa_filtro:
        reportes = reportes.filter(programa__icontains=programa_filtro)
    if estado_filtro:
        reportes = reportes.filter(estado__iexact=estado_filtro)
        
    return render(request, "gestion_reportes.html", {
        "reportes": reportes,
        "profesor_filtro": profesor_filtro,
        "programa_filtro": programa_filtro,
        "estado_filtro": estado_filtro,
    })


def consulta_profesor(request):
    profesor = None
    reportes = None
    error = None
    
    if request.method == "POST":
        nombre_ingresado = request.POST.get("nombre", "").strip()
        token_ingresado = request.POST.get("token", "").strip()
        
        profesor = Profesor.objects.filter(nombre__iexact=nombre_ingresado, token=token_ingresado).first()
        if profesor:
            reportes = Registro.objects.filter(profesor=profesor, eliminado=False).order_by('-fecha')
        else:
            error = "Credenciales incorrectas. Verifique que su nombre esté escrito exactamente igual al registro."
            
    return render(request, "consulta_profesor.html", {"profesor": profesor, "reportes": reportes, "error": error})