from django.db import models

from app.services.api.dolarblue.dolarblue import DolarBlueClient
from app.services.api.dolarblue.errors import DolarBlueError


class Order(models.Model):

    date_time = models.DateTimeField()

    def get_total(self) -> float:
        return round(sum(details.sub_total for details in self.details.all()), 2)

    def get_total_usd(self) -> float:
        total = self.get_total()
        dolarsi_client = DolarBlueClient()
        try:
            dolar_blue_price = dolarsi_client.getCurrentDolarBluePrice()
        except DolarBlueError:
            dolar_blue_price = None

        if dolar_blue_price and total:
            return round(total/float(dolar_blue_price), 2)
        return None

    def __str__(self):
        return f"ID: {self.id} total: ${self.get_total()} total usd:${self.get_total_usd()}"
