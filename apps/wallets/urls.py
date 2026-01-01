from django.urls import path

from apps.wallets.views import (
    student_wallets,
    recharge_student_wallet,
    generate_daily_quota
)

urlpatterns = [
    path("student-wallets/", student_wallets, name="student-wallets"),
    path("recharge-wallet/", recharge_student_wallet, name="recharge-wallet"),
    path("generate-daily-quotas/", generate_daily_quota, name="generate-daily-quotas"),
]