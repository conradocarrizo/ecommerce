from rest_framework import serializers

from app.models.order_detail import OrderDetail
from app.serializers.product import ProductSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    sub_total = serializers.ReadOnlyField()
    product = ProductSerializer(required=False)
    pk = serializers.IntegerField(required=False)

    class Meta:
        model = OrderDetail
        fields = ['pk',"quantity", "sub_total",'product']
        depth = 3

    def get_sub_total(self, obj: OrderDetail):
        return obj.sub_total
