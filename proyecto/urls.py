from django.contrib import admin
from django.urls import path
from core import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('gestion_reportes')), 
    path('gestion-tokens/', views.gestion_tokens, name='gestion_tokens'),
    path('gestion-reportes/', views.gestion_reportes, name='gestion_reportes'),
    path('consulta/', views.consulta_profesor, name='consulta'),
]