from django.contrib import admin

from apps.students.models import Student, StudentWallet, WalletRechargeLog


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display= ["registration_number", "status", "student_type"]

admin.site.register(StudentWallet)

@admin.register(WalletRechargeLog)
class WalletRechargeLogAdmin(admin.ModelAdmin):
    list_display = ["student", "wallet", "recharge_method", "amount_recharged"]