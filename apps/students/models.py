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


    def __str__(self):
        return self.registration_number

    @property
    def wallet_balance(self):
        return self.studentwallet.balance


class StudentWallet(AbstractBaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="studentwallet")
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    total_spend_today = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.student.registration_number

    def today_quota_generated(self):
        return True if self.modified.date() == date_today else False


    def spend_today(self):
        student_oders = sum(self.student.studentorders.filter(status="Processed", created__date=date_today).values_list("total_cost", flat=True))
        return student_oders

RECHARGE_METHODS = (
    ("Mpesa", "Mpesa"),
    ("Cash", "Cash"),
)

class WalletRechargeLog(AbstractBaseModel):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    wallet = models.ForeignKey(StudentWallet, on_delete=models.SET_NULL, null=True)
    recharge_method = models.CharField(max_length=255, choices=RECHARGE_METHODS)
    amount_recharged = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.student.registration_number