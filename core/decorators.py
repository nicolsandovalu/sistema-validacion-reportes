from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def tiene_rol(user, *roles):
    return user.groups.filter(name__in=roles).exists() or user.is_superuser

def requiere_rol(*roles):
    def decorador(view_func):
        @wraps(view_func)
        @login_required(login_url='login') # Redirige al login si no hay sesión
        def wrapper(request, *args, **kwargs):
            if tiene_rol(request.user, *roles):
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permiso para esta acción.")
            return redirect('consulta')
        return wrapper
    return decorador