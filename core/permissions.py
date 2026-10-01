from rest_framework import permissions

class SoloStaffBorra(permissions.BasePermission):
    """Cualquiera autenticado lee y crea; borrar es solo del staff."""
    
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return request.user.is_staff
        return request.user.is_authenticated