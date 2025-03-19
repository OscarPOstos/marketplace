from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configurar la vista de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Marketplace API",
        default_version="v1",
        description="Documentación de la API del Marketplace de Servicios",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path('api/services/', include('services.urls')),
    path('api/bookings/', include('bookings.urls')),
    # Documentación Swagger y Redoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]