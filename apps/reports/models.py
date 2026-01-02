from django.db import models
from decimal import Decimal
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
    order = order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)

    def __str__(self):
        return str(self.id)


class SalesReport(AbstractBaseModel):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    item = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    sold_or_spoiled = models.CharField(max_length=255, choices=SOLD_OR_SPOILED_CHOICES, null=True)
    quantity = models.FloatField(default=0)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)

    def __str__(self):
        return str(self.id)

class GeneralisedReportData(AbstractBaseModel):
    item = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    sold_or_spoiled = models.CharField(max_length=255, choices=SOLD_OR_SPOILED_CHOICES, null=True)
    quantity = models.FloatField(default=0)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)

    def __str__(self):
        return str(self.id)


class DailySalesReportData(AbstractBaseModel):
    date_recorded = models.DateTimeField(null=True)
    item = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    sold_or_spoiled = models.CharField(max_length=255, choices=SOLD_OR_SPOILED_CHOICES, null=True)
    quantity = models.FloatField(default=0)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)

    def __str__(self):
        return str(self.id)