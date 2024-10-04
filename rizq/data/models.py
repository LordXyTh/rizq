from django.db import models

# Create your models here.
# portfolio/models.py


class IndexStock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, blank=True)
    price = models.FloatField(null=True, blank=True)
    market_cap = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.symbol}"
