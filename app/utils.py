from requests import Response
from rest_framework.views import exception_handler

from app.errors import InvalidProductStock, InvalidQuantityError, NotEnoughtStockError, DuplicateProductDetailOrdenError
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, DuplicateProductDetailOrdenError):
        return Response({"error": exc.message}, status=400)
    
    if isinstance(exc, InvalidQuantityError):
        return Response({"error": exc.message}, status=400)

    if isinstance(exc, InvalidProductStock):
        return Response({"error": exc.message}, status=400)

    if isinstance(exc, NotEnoughtStockError):
        return Response({"error": exc.message}, status=400)
