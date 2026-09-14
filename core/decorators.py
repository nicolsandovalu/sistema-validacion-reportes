from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def tiene_rol(user, *roles):
    # Consulta real a la base de datos para verificar el grupo del usuario
    return user.groups.filter(name__in=roles).exists() or user.is_superuser

def requiere_rol(*roles):
    def decorador(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def wrapper(request, *args, **kwargs):
            if tiene_rol(request.user, *roles):
                return view_func(request, *args, **kwargs)
            messages.error(request, "Acceso denegado: No tienes los permisos necesarios.")
            return redirect('login')
        return wrapper
    return decorador