from django.db import models

from apps.core.models import AbstractBaseModel

# Create your models here.
ORDER_STATUS_CHOICES = (
    ("Cancelled", "Cancelled"),
    ("Processed", "Processed"),
    ("Pending", "Pending"),
    ("Nullified", "Nullified"),
)


PAYMENT_METHODS = (
    ("Mpesa", "Mpesa"),
    ("Cash", "Cash"),
    ("Wallet", "Wallet"),
    ("Wallet And Cash", "Wallet And Cash"),
    ("Wallet And Mpesa", "Wallet And Mpesa"),
)

class Order(AbstractBaseModel):
    student = models.ForeignKey("students.Student", on_delete=models.SET_NULL, null=True, related_name="studentorders")
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    meal_time = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES)
    served_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=255, null=True, choices=PAYMENT_METHODS)

    def __str__(self):
        return str(self.id)


class OrderItem(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    item = models.ForeignKey("inventory.Menu", on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class TemporaryOrderItem(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    menu_item = models.OneToOneField("inventory.Menu", on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.menu_item.item

class TemporaryCustomerOrderItem(AbstractBaseModel):
    #student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    menu_item = models.OneToOneField("inventory.Menu", on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.menu_item.item       