from rest_framework import serializers
from app.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    total_usd = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['date_time', 'total', 'total_usd', 'details']
        depth = 2

    def get_total(self, obj: Order):
        return obj.get_total()

    def get_total_usd(self, obj: Order):
        return obj.get_total_usd()
