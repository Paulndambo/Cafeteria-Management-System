from django.db import models
from apps.core.models import AbstractBaseModel
from datetime import datetime
# Create your models here.

date_today = datetime.now().date()

class StudentWallet(AbstractBaseModel):
    student = models.OneToOneField("students.Student", on_delete=models.CASCADE, related_name="studentwallet")
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
    student = models.ForeignKey("students.Student", on_delete=models.SET_NULL, null=True)
    wallet = models.ForeignKey(StudentWallet, on_delete=models.SET_NULL, null=True)
    recharge_method = models.CharField(max_length=255, choices=RECHARGE_METHODS)
    amount_recharged = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.student.registration_number
    


class OrderPayment(AbstractBaseModel):
    student = models.ForeignKey("students.Student", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return self.student.registration_number