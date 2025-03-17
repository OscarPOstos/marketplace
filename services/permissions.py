from rest_framework import permissions

class IsProfessional(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'professional'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'professional'

class IsOwner(permissions.BasePermission):
    """
    Permite edición/eliminación solo al dueño del servicio.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user