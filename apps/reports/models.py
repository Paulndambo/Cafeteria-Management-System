from django.db import models

from apps.core.models import AbstractBaseModel

# Create your models here.
PAYMENT_METHODS = (
    ("Mpesa", "Mpesa"),
    ("Cash", "Cash"),
    ("Wallet", "Wallet"),
)

class SalesReport(AbstractBaseModel):
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.id)