from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Cliente'),
        ('professional', 'Profesional'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username
