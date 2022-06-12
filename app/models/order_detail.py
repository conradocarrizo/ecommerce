from django.db import models
from app.models.order import Order
from app.models.product import Product


class OrderDetail(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="details", null=True)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products", null=True)

    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"], name='order_product'),
        ]

    @property
    def sub_total(self) -> float:
        return self.product.price * self.quantity

    def __str__(self):
        return f"ID: {self.order_id} subtotal:${self.sub_total} quantity: {self.product.name} product:{self.quantity}"
