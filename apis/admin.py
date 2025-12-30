from django.contrib import admin

from apis.models import VerificationCode, MpesaTransaction
# Register your models here.
@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'student', 'is_verified', 'created')


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'merchant_request_id', 'checkout_request_id', 'amount', 'mpesa_receipt_number', 'phone_number', 'result_code', 'result_desc', 'created')