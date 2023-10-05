from django.db import models

from apps.core.constants import UNIT_CHOICES
from apps.core.models import AbstractBaseModel


# Create your models here.
class Supplier(AbstractBaseModel):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    postal_address = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    @property
    def address(self):
        return f"{self.postal_address}, {self.town}-{self.country}"

class Inventory(AbstractBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class StockLog(AbstractBaseModel):
    actioned_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=255, null=True)
    destination = models.CharField(max_length=255, null=True)
    

    def __str__(self):
        return self.inventory.name


class Menu(AbstractBaseModel):
    #item = models.OneToOneField(Inventory, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name