from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Registra un nuevo usuario (Cliente o Profesional)",
        request_body=RegisterSerializer,
        responses={201: UserSerializer(), 400: "Error de validación"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Inicia sesión y devuelve un token JWT",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre de usuario"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Contraseña"),
            },
            required=["username", "password"],
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Token de refresco"),
                "access": openapi.Schema(type=openapi.TYPE_STRING, description="Token de acceso"),
            },
        ), 401: "Credenciales inválidas"},
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Devuelve el usuario autenticado"""
        return self.request.user

    @swagger_auto_schema(
        operation_description="Obtiene la información del usuario autenticado",
        responses={200: UserSerializer(), 401: "No autorizado"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza el perfil del usuario autenticado",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Error de validación"},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina la cuenta del usuario autenticado",
        responses={204: "Usuario eliminado", 401: "No autorizado"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)