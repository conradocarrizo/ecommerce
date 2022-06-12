class DolarSiError(Exception):
    message: str = ""

    def __init__(self, message=""):
        if message:
            self.message = message

    def __str__(self):
        return self.message
