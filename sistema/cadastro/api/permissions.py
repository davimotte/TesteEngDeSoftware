from rest_framework.permissions import BasePermission

class IsAdminClinica(BasePermission):
    def has_permission(self, request, view):
        # integrar com  JWT/perfil (ADMIN_CLINICA) depois.
        # todos liberados por enquanto
        return True
