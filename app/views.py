from rest_framework import viewsets
from rest_framework.response import Response
from app.models.order import Order
from app.models.product import Product
from app.serializers.order import OrderSerializer

from app.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response({"message": "Product has been deleted"}, status=204)

class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
