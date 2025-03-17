from django.db import models
from django.conf import settings

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tecnología'),
        ('design', 'Diseño'),
        ('marketing', 'Marketing'),
        ('other', 'Otros'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
