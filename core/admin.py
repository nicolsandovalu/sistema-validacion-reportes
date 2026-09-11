from django.contrib import admin
from django.core.mail import send_mail
from .models import Profesor, Registro

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "token")
    search_fields = ("nombre",)
    readonly_fields = ("token",)

    # Dispara el correo SOLO cuando se inscribe al profesor por primera vez
    def save_model(self, request, obj, form, change):
        es_nuevo = obj.pk is None
        super().save_model(request, obj, form, change)
        
        if es_nuevo:
            send_mail(
                subject='Bienvenido: Su Token de Acceso Académico',
                message=f'Estimado/a {obj.nombre},\n\nSu perfil ha sido creado. Su token de acceso único y permanente es: {obj.token}\nÚselo para consultar su historial de reportes.',
                from_email='coordinacion@institucion.cl',
                recipient_list=[obj.correo],
                fail_silently=True,
            )

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ("get_profesor_nombre", "programa", "estado", "pago_profesores", "resultado", "fecha")
    list_filter = ("estado", "programa", "eliminado")
    search_fields = ("profesor__nombre",)
    
    # Muestra el nombre del profesor en la tabla de reportes
    def get_profesor_nombre(self, obj):
        return obj.profesor.nombre
    get_profesor_nombre.short_description = 'Profesor'