from django.db import models

from apps.core.models import AbstractBaseModel

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


class StudentWallet(AbstractBaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="studentwallet")
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    total_spend_today = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.student.registration_number