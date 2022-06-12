from logging import exception
from app.services.api.base_request import BaseRequest
from app.services.api.dolarsi.errors import DolarSiError


CURRENT_DOLAR_BLUE_PRICE_ENDPOINT = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
DOLAR_BLUE = "Dolar Blue"


class DolarSiClient(object):
    """
     api for the dolarsi service  https://www.dolarsi.com/api/api.php?type=valoresprincipales
    """
    request = None

    def getCurrentDolarBluePrice(self):
        try:
            self.request = BaseRequest(url=CURRENT_DOLAR_BLUE_PRICE_ENDPOINT)
            response = self.request.get()
            dolar_blue_price = next(
                (
                    casa["casa"]["venta"]
                    for casa in response.json()
                    if casa.get("casa").get("nombre") == DOLAR_BLUE
                ),
                None,
            )
            if not dolar_blue_price:
                raise DolarSiError(
                    message="Could not get dolar blue price")

            return dolar_blue_price.replace(",", ".")

        except Exception:
            raise DolarSiError(message="Could not connect with the api service")
