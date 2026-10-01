from rest_framework import viewsets
from .models import Registro
from .serializers import RegistroSerializer
from .permissions import SoloStaffBorra

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.filter(eliminado=False).order_by("-fecha")  # pylint: disable=no-member
    
    # Esta es la línea que Django no está encontrando:
    serializer_class = RegistroSerializer
    
    permission_classes = [SoloStaffBorra]

    def perform_create(self, serializer):
        serializer.save(estado="Activo")