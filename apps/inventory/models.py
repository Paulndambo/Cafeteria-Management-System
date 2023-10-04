from django.db import models
from apps.core.models import AbstractBaseModel
from apps.core.constants import UNIT_CHOICES

# Create your models here.
class Inventory(AbstractBaseModel):
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class StockLog(AbstractBaseModel):
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.inventory.name