from requests import Response
from rest_framework.views import exception_handler

from app.errors import InvalidStockProduct
from rest_framework.response import Response

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, InvalidStockProduct):
        return Response({"error": exc.message}, status=400)