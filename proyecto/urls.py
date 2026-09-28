from django.contrib import admin
from django.urls import path, include  # Agregamos include aquí
from core import views
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from core.api_views import RegistroViewSet

router = DefaultRouter()
router.register(r"registros", RegistroViewSet, basename="registro")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('gestion_reportes')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    path('api/', include(router.urls)),
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    
    # --- Tus rutas existentes (EVA2) ---
    path('gestion-tokens/', views.gestion_tokens, name='gestion_tokens'),
    path('gestion-reportes/', views.gestion_reportes, name='gestion_reportes'),
    path('consulta/', views.consulta_profesor, name='consulta'),
    path('eliminar/<int:pk>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('editar/<int:pk>/', views.editar_reporte, name='editar_reporte'),
]