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
    amount_owed = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    total_supplies_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    @property
    def address(self):
        return f"{self.postal_address}, {self.town}-{self.country}"

class SupplyLog(AbstractBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="mysupplies")
    item = models.CharField(max_length=255)
    quantity_supplied = models.FloatField(default=0)
    unit_price = models.DecimalField(max_digits=200, decimal_places=2)
    payment_method = models.CharField(max_length=255, null=True)
    total_cost = models.DecimalField(max_digits=100, decimal_places=2)
    supply_unit = models.CharField(max_length=255, null=True)


    def __str__(self):
        return self.name


class Inventory(AbstractBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name="supplies")
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=255, null=True)

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

MENU_CATEGOGIES = (
    ("drinks", "Drinks"),
    ("food", "Food"),
    ("fruits", "Fruits"),
)

class Menu(AbstractBaseModel):
    #item = models.OneToOneField(Inventory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="menu_images", null=True)
    category = models.CharField(max_length=255, choices=MENU_CATEGOGIES, null=True)
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    added_to_cart = models.BooleanField(default=False)
    quantity = models.FloatField(default=0)
    starting_stock = models.FloatField(default=0)

    def __str__(self):
        return self.item
