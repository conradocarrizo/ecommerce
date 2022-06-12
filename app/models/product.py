import uuid
from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} price: ${self.price} stock:{self.stock}"
