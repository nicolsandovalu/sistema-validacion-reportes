from rest_framework import serializers
from .models import Registro

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        # Incluimos el "id" de forma obligatoria y todos los campos relevantes de tu modelo
        fields = ["id", "profesor", "programa", "estado", "cantidad", "ventas_totales", "isn", "nps", "cantidad_respuestas"]
        
        # Bloqueamos el estado para que el cliente no pueda inyectar valores como "Activo" o "Aceptado"
        read_only_fields = ["estado"]