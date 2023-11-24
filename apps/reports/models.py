from django.db import models

from apps.core.models import AbstractBaseModel

# Create your models here.
PAYMENT_METHODS = (
    ("Mpesa", "Mpesa"),
    ("Cash", "Cash"),
    ("Wallet", "Wallet"),
    ("No Payment", "No Payment"),
)

SOLD_OR_SPOILED_CHOICES = (
    ("Sold", "Sold"),
    ("Spoiled", "Spoiled"),
)

class DailySalesReport(AbstractBaseModel):
    order = order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.id)


class SalesReport(AbstractBaseModel):
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True)
    item = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    sold_or_spoiled = models.CharField(max_length=255, choices=SOLD_OR_SPOILED_CHOICES, null=True)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)