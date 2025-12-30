from django.db import models

from apps.core.models import AbstractBaseModel
# Create your models here.
class VerificationCode(AbstractBaseModel):
    code = models.CharField(max_length=6)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='verificationcodes')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Code: {self.code} for Student ID: {self.student.id}"
    


class MpesaTransaction(AbstractBaseModel):
    merchant_request_id = models.CharField(max_length=255, null=True, blank=True)
    checkout_request_id = models.CharField(max_length=255, null=True, blank=True)
    response_desc = models.CharField(max_length=255, null=True, blank=True)
    customer_message = models.CharField(max_length=255, null=True, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_desc = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mpesa_receipt_number = models.CharField(max_length=20, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_date = models.CharField(max_length=14, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"M-Pesa Transaction {self.mpesa_receipt_number} - {self.result_desc}"