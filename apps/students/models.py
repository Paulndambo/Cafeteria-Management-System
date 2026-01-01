from datetime import datetime

from django.db import models

from apps.core.models import AbstractBaseModel

date_today = datetime.now().date()

# Create your models here.
STUDENT_TYPES = (
    ("Boarder", "Boarding Student"),
    ("Prepaid", "Prepaid Student"),
    ("One-Time", "Pay-As-You Go Student"),
)

STUDENT_STATUS = (
    ("Active", "Active"),
    ("Deactivated", "Deactivated"),
    ("Suspended", "Suspended"),
)

class Student(AbstractBaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    student_type = models.CharField(max_length=255, choices=STUDENT_TYPES)
    registration_number = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STUDENT_STATUS)
    added_on = models.DateField(null=True)
    credit_limit = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    quota_group = models.ForeignKey("core.QuotaGroup", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.registration_number

    @property
    def wallet_balance(self):
        return self.studentwallet.balance

    @property
    def total_orders(self):
        return self.studentorders.count()

