from rest_framework import generics, filters, permissions
from .models import Service
from .serializers import ServiceSerializer
from .permissions import IsProfessional, IsOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Listar y crear servicios
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsProfessional()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_description="Lista todos los servicios con opción de filtrar por categoría, precio, etc.",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Buscar por título o descripción", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordenar por precio o fecha", type=openapi.TYPE_STRING)
        ],
        responses={200: ServiceSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo servicio (solo profesionales)",
        request_body=ServiceSerializer,
        responses={201: ServiceSerializer(), 403: "No autorizado"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Obtener, actualizar o eliminar un servicio específico
class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsOwner()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_description="Obtiene detalles de un servicio específico",
        responses={200: ServiceSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Edita un servicio (solo el profesional dueño)",
        request_body=ServiceSerializer,
        responses={200: ServiceSerializer(), 403: "No autorizado"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina un servicio (solo el profesional dueño)",
        responses={204: "Servicio eliminado", 403: "No autorizado"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)