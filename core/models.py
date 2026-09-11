import secrets
from django.db import models
from django.utils import timezone

class Profesor(models.Model):
    # unique=True evita duplicados y genera la alerta automática
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre Exacto")
    correo = models.EmailField(default="profesor@institucion.cl")
    token = models.CharField(max_length=10, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.token: # Se genera una única vez al crearlo
            self.token = secrets.token_hex(3).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Registro(models.Model):
    # Relacionamos el reporte con el profesor (permite tener historial de varios meses)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="reportes")
    programa = models.CharField(max_length=150, default="Sin Programa")
    cantidad = models.IntegerField(verbose_name="Horas/Cantidad", default=0)
    estado = models.CharField(max_length=50)
    
    pago_profesores = models.IntegerField(default=0)
    ventas_totales = models.IntegerField(default=0)
    cantidad_respuestas = models.IntegerField(default=0)
    isn = models.IntegerField(default=0)
    nps = models.IntegerField(default=0)
    
    resultado = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)

    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()