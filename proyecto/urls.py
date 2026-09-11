from django.contrib import admin
from django.urls import path
from core import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('gestion_reportes')), 
    
    # Rutas de autenticación propias
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    
    # Tus rutas existentes
    path('gestion-tokens/', views.gestion_tokens, name='gestion_tokens'),
    path('gestion-reportes/', views.gestion_reportes, name='gestion_reportes'),
    path('consulta/', views.consulta_profesor, name='consulta'),
    path('eliminar/<int:pk>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('editar/<int:pk>/', views.editar_reporte, name='editar_reporte'),
]