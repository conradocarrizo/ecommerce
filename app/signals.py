from django.dispatch import receiver
from app.errors import InvalidStockProduct
from app.models.order_detail import OrderDetail
from django.db.models.signals import pre_save, post_delete

from app.models.product import Product


@receiver(pre_save, sender=OrderDetail, weak=False, dispatch_uid="pre_save_update_stock")
def pre_save_update_stock(sender, instance: OrderDetail, **kwargs):

    new_quantity = instance.quantity

    if not instance._state.adding and instance.pk:
        prev_quantity = sender.objects.get(id=instance.pk).quantity
        if new_quantity < prev_quantity:
            difference = prev_quantity - new_quantity
            instance.product.stock = instance.product.stock + difference
        else:
            difference = new_quantity - prev_quantity
            instance.product.stock = instance.product.stock - difference

    else:
        instance.product.stock = instance.product.stock - new_quantity
    instance.product.save(update_fields=["stock"])


@receiver(post_delete, sender=OrderDetail, weak=False, dispatch_uid="post_delete_update_stock")
def post_delete_update_stock(sender, instance: OrderDetail, **kwargs):
    quantity_to_restore = instance.quantity
    instance.product.stock = instance.product.stock + quantity_to_restore
    instance.product.save(update_fields=["stock"])


@receiver(pre_save, sender=Product, weak=False, dispatch_uid="pre_save_validate_product")
def pre_save_validate_product(sender, instance: Product, **kwargs):
    if instance.stock < 0:
        raise InvalidStockProduct(instance.stock)