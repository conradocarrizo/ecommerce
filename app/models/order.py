from django.db import models


class Order(models.Model):

    date_time = models.DateTimeField()

    def get_total(self) -> float:
        return sum(details.sub_total for details in self.details.all())

    def get_total_usd(self):
        pass

    def __str__(self):
        return f"ID: {self.id} total: ${self.get_total()}"
