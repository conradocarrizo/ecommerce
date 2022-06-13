from rest_framework import serializers

from app.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)

    class Meta:
        model = Product
        fields = '__all__'
