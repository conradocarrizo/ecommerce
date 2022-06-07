import stat
from django.db import models


class Order(models.Model):

    date_time = models.DateTimeField()

    def get_total(self):
        pass

    def get_total_usd(self):
        pass
