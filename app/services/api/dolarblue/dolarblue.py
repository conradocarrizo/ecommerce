from app.services.api.base_request import BaseRequest
from app.services.api.dolarblue.errors import DolarBlueError
import requests_cache


CURRENT_DOLAR_BLUE_PRICE_ENDPOINT = "https://api-dolar-argentina.herokuapp.com/api/dolarblue"


class DolarBlueClient(object):
    """
     api for the dolarsi service  https://api-dolar-argentina.herokuapp.com/
    """
    request = None

    def getCurrentDolarBluePrice(self):
        try:
            self.request = BaseRequest(url=CURRENT_DOLAR_BLUE_PRICE_ENDPOINT)
            with requests_cache.enabled():
                response = self.request.get()
            respose_dict = response.json()
            dolar_blue_price = respose_dict.get("venta")

            if not dolar_blue_price:
                raise DolarBlueError(
                    message="Could not get dolar blue price")

            return dolar_blue_price

        except Exception:
            raise DolarBlueError(
                message="Could not connect with the api service")
