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


    def spend_today(self):
        student_oders = sum(self.student.studentorders.filter(status="Processed", created__date=date_today).values_list("total_cost", flat=True))
        return student_oders