from django.db import models


class Product(models.Model):

    id = models.CharField(primary_key=True, unique=True, max_length=100)
    name = models.CharField(max_length=150, blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
