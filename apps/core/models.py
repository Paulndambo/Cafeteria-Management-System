from django.db import models


# Create your models here.
class AbstractBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tenant(models.Model):
    pass

PAYMENTS_STATUS_CHOICES = (
    ("paid", "Paid"),
    ("future", "Future"),
    ("pending", "Pending"),
    ("unpaid", "Unpaid"),
    ("disputed", "Disputed"),
)

class TenantPremiums(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="payments")
    month = models.CharField(max_length=255)
    amount_expected = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, choices=PAYMENTS_STATUS_CHOICES)
    

class Payment(models.Model):
    pass

class Expense(AbstractBaseModel):
    title = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title