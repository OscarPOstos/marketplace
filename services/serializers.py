from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Service
        fields = '__all__'