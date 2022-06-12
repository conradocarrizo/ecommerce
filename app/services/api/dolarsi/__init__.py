from app.services.api.base_request import BaseRequest


class DolarSiClient(object):
    """
     api for the dolarsi service  https://www.dolarsi.com/api/api.php?type=valoresprincipales
    """
    CURRENT_DOLAR_BLUE_PRICE_ENDPOINT = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
    request = None

    def getCurrentDolarBluePrice(self):
        request = BaseRequest(url=self.CURRENT_DOLAR_BLUE_PRICE_ENDPOINT)
        response = request.get()
        return response
