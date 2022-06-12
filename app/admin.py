from django.contrib import admin
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product import Product

admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Product)