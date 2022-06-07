from pyexpat import model
from django.db import models
from app.models.order import Order
from app.models.product import Product


class OrderDetail(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order", null=True)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products", null=True)

    quantity = models.IntegerField()
