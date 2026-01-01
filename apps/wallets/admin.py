from django.contrib import admin
from apps.wallets.models import StudentWallet, WalletRechargeLog

@admin.register(StudentWallet)
class StudentWalletAdmin(admin.ModelAdmin):
    list_display = ["student", "balance", "total_spend_today"]
    #search_fields = ["student", "balance"]
    list_filter = ["balance"]


@admin.register(WalletRechargeLog)
class WalletRechargeLogAdmin(admin.ModelAdmin):
    list_display = ["student", "wallet", "recharge_method", "amount_recharged"]

