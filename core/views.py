import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profesor, Registro
from .decorators import requiere_rol
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

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
            
            # Validación estricta de estado (Punto 3 de la rúbrica)
            estado_csv = fila.get('Estado', '').strip()
            if estado_csv not in ["Activo", "Deprecado"]:
                errores.append(f"{nombre_reporte} (Estado inválido)")
                continue
            
            # Validación de integridad numérica
            try:
                cantidad = int(fila.get('Cantidad de Respuestas', 0) or 0)
                pago = int(fila.get('Pago Profesores', 0) or 0)
                ventas = int(fila.get('Ventas Totales', 0) or 0)
                isn_val = int(fila.get('ISN', 0) or 0)
                nps_val = int(fila.get('NPS', 0) or 0)
                
                # Bloquear valores negativos
                if cantidad < 0 or pago < 0 or ventas < 0:
                    errores.append(f"{nombre_reporte} (Valores negativos)")
                    continue
                    
            except ValueError:
                messages.error(request, "Error de formato: Se detectaron caracteres inválidos en las columnas numéricas del archivo.")
                return redirect('gestion_reportes')
                
            Registro.objects.create(
                profesor=profesor,
                programa=fila.get('Programa', '').strip(),
                cantidad=cantidad,
                estado=estado_csv,
                pago_profesores=pago,
                ventas_totales=ventas,
                cantidad_respuestas=cantidad,
                isn=isn_val,
                nps=nps_val,
                resultado="" 
            )
            creados += 1
            
        if errores:
            nombres_unicos = set(errores)
            messages.warning(request, f"Se cargaron {creados} reportes. OMITIDOS por errores de datos o formato: {', '.join(nombres_unicos)}")
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


# --- NUEVAS VISTAS PARA CUMPLIR LA RÚBRICA 2.1.3 (OPERACIONES CRUD) ---

@requiere_rol("admin")
def eliminar_reporte(request, pk):
    registro = get_object_or_404(Registro, pk=pk, eliminado=False)
    if request.method == "POST":
        registro.soft_delete()
        messages.success(request, "Registro eliminado del sistema.")
        return redirect('gestion_reportes')
    return render(request, "confirmar.html", {"registro": registro})


@requiere_rol("admin")
def editar_reporte(request, pk):
    registro = get_object_or_404(Registro, pk=pk, eliminado=False)
    
    if request.method == "POST":
        print("\n=== DEBUG DE SEGURIDAD: INICIO DE POST ===")
        print(f"Diccionario POST completo recibido: {request.POST}")
        
        try:
            # 1. Validación de Estado con trazabilidad
            estado_nuevo = request.POST.get("estado", registro.estado).strip()
            print(f"Estado capturado por el servidor: '{estado_nuevo}'")
            
            if estado_nuevo not in ["Activo", "Deprecado"]:
                print(">> ALERTA: Estado inválido detectado. Bloqueando guardado y retornando error.")
                messages.error(request, "Error: El estado debe ser estrictamente 'Activo' o 'Deprecado'.")
                return render(request, "editar.html", {"registro": registro})
            
            print(">> EXITO: Estado válido. Continuando con el guardado...")
            
            # 2. Captura de datos numéricos segura
            val_cantidad = request.POST.get("cantidad")
            cantidad_nueva = int(val_cantidad) if val_cantidad != "" else registro.cantidad
            
            if cantidad_nueva < 0:
                messages.error(request, "Error: La cantidad ingresada debe ser un número positivo.")
                return render(request, "editar.html", {"registro": registro})
            
            # 3. Asignaciones
            registro.estado = estado_nuevo
            registro.programa = request.POST.get("programa", registro.programa).strip()
            registro.resultado = request.POST.get("resultado", registro.resultado or "").strip()
            
            registro.cantidad = cantidad_nueva
            if hasattr(registro, 'cantidad_respuestas'):
                registro.cantidad_respuestas = cantidad_nueva
            
            val_ventas = request.POST.get("ventas_totales")
            registro.ventas_totales = int(val_ventas) if val_ventas != "" else registro.ventas_totales
            
            val_isn = request.POST.get("isn")
            registro.isn = int(val_isn) if val_isn != "" else registro.isn
            
            val_nps = request.POST.get("nps")
            registro.nps = int(val_nps) if val_nps != "" else registro.nps
            
            registro.save()
            print("=== DEBUG DE SEGURIDAD: GUARDADO EXITOSO ===\n")
            messages.success(request, "Registro actualizado correctamente en el sistema.")
            return redirect('gestion_reportes')
            
        except ValueError:
            messages.error(request, "Error: Verifique que los campos numéricos (cantidad, ventas, ISN, NPS) contengan solo números.")
            return render(request, "editar.html", {"registro": registro})
            
    return render(request, "editar.html", {"registro": registro})


def vista_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", "")
        )
        if user:
            auth_login(request, user)
            return redirect("gestion_reportes")
        messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")


def vista_logout(request):
    auth_logout(request)
    return redirect("login")