from rest_framework.exceptions import APIException

class InvalidStockProduct(Exception):
    message: str = "the stock must be a positive number"

    def __init__(self, stock=None):
        if stock:
            self.message = self.message + f", {stock} is not"

    def __str__(self):
        return self.message
