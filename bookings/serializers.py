from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    service_title = serializers.ReadOnlyField(source='service.title')

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, attrs):
        """
        Permite actualizar sin requerir `service` ni `date`.
        """
        request = self.context.get('request')
        if request and request.method == 'POST':  # Solo en creación (POST) son obligatorios
            if 'service' not in attrs or 'date' not in attrs:
                raise serializers.ValidationError("Los campos 'service' y 'date' son obligatorios.")
        return attrs