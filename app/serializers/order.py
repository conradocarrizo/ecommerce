from rest_framework import serializers
from app.errors import DuplicatedProductDetailOrdenError
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.serializers.order_detail import OrderDetailSerializer
from django.db import IntegrityError, transaction


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    total_usd = serializers.SerializerMethodField()
    details = OrderDetailSerializer(many=True, required=False)
    
    class Meta:
        model = Order
        fields = ['id', 'date_time', 'total', 'total_usd', 'details']
        depth = 3

    def get_total(self, obj: Order):
        return obj.get_total()

    def get_total_usd(self, obj: Order):
        return obj.get_total_usd()

    def create(self, validated_data):
        instance = Order.objects.create(date_time=validated_data.get("date_time"))
        for detail in validated_data["details"]:
            try:
                OrderDetail.objects.create(
                    order=instance,
                    product_id=detail.get("product").get("id"),
                    quantity=detail.get("quantity")
                )
            except IntegrityError as error:
                if "UNIQUE constraint failed" in str(error):
                    raise DuplicatedProductDetailOrdenError(
                        product_name=detail.get("product").get("name"))
                else:
                    raise error
        instance.refresh_from_db()
        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            date_time = validated_data.get("date_time")
            if instance.date_time != date_time:
                instance.date_time = date_time
                instance.save()

            for detail in validated_data["details"]:
                if detail.get("pk"):
                    order_detail = OrderDetail.objects.get(id=detail["pk"])
                    if order_detail and order_detail.quantity != detail.get("quantity"):
                        order_detail.quantity = detail.get("quantity")
                        order_detail.save()
                else:
                    try:
                        OrderDetail.objects.create(
                            order=instance,
                            product_id=detail.get("product").get("id"),
                            quantity=detail.get("quantity")
                        )
                    except IntegrityError as error:
                        if "UNIQUE constraint failed" in str(error):
                            raise DuplicatedProductDetailOrdenError(
                                product_name=detail.get("product").get("name"))
                        else:
                            raise error
        instance.refresh_from_db()
        return instance
