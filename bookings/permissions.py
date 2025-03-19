from rest_framework import permissions

class IsOwnerOrProfessional(permissions.BasePermission):
    """
    Permite acceso solo al usuario que hizo la reserva o al profesional dueño del servicio.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.service.owner == request.user