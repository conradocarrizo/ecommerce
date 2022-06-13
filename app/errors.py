class InvalidProductStock(Exception):
    message: str = "the stock must be a positive number"

    def __init__(self, stock=None):
        if stock:
            self.message = self.message + f", {stock} is not"

    def __str__(self):
        return self.message


class InvalidQuantityError(Exception):
    message: str = "the quantity must be a greater than 0"

    def __init__(self, quantity=None):
        if quantity:
            self.message = self.message + f", {quantity} is not"

    def __str__(self):
        return self.message


class NotEnoughtStockError(Exception):
    message: str = "not enought stock"

    def __init__(self, product_name=None):
        if product_name:
            self.message = self.message + f" of {product_name}"

    def __str__(self):
        return self.message


class DuplicateProductDetailOrdenError(Exception):
    message: str = "There can only be one detail order for each product in the order"

    def __init__(self, product_name=None):
        if product_name:
            self.message = self.message + f"{product_name} more than once"

    def __str__(self):
        return self.message
