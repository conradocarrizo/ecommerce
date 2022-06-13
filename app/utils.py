from requests import Response
from rest_framework.views import exception_handler
from rest_framework import status

from app.errors import InvalidProductStock, InvalidQuantityError, NotEnoughtStockError, DuplicateProductDetailOrdenError
from rest_framework.response import Response


CUSTOM_400_ERRORS = [InvalidProductStock, InvalidQuantityError,
                     NotEnoughtStockError, DuplicateProductDetailOrdenError]


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if response is not None:
        return response

    if type(exc) in CUSTOM_400_ERRORS:
        return Response({"error": exc.message}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"error": format(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
