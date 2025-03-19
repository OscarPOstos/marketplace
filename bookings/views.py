from rest_framework import generics, permissions
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsOwnerOrProfessional
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Listar y crear reservas
class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        """Lista solo las reservas del usuario autenticado"""
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Lista todas las reservas del usuario autenticado",
        responses={200: BookingSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva reserva",
        request_body=BookingSerializer,
        responses={201: BookingSerializer(), 403: "No autorizado"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Obtener, actualizar o eliminar una reserva específica
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrProfessional]

    @swagger_auto_schema(
        operation_description="Obtiene detalles de una reserva específica",
        responses={200: BookingSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza el estado de una reserva",
        request_body=BookingSerializer,
        responses={200: BookingSerializer(), 403: "No autorizado"}
    )
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cancela una reserva",
        responses={204: "Reserva cancelada", 403: "No autorizado"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
