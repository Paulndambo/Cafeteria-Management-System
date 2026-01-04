from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.wallets.models import StudentWallet, WalletRechargeLog
from django.http import HttpRequest
date_today = datetime.now().date()
# Create your views here.

@login_required(login_url="/users/login/")
def student_wallets(request: HttpRequest):
    wallets = StudentWallet.objects.all()

    if request.method == "POST":
        reg_number = request.POST.get("reg_number")
        wallets = StudentWallet.objects.filter(
            Q(student__registration_number__icontains=reg_number) |
            Q(student__user__id_number__icontains=reg_number) |
            Q(student__user__first_name__icontains=reg_number) |
            Q(student__user__last_name__icontains=reg_number)
        )

    paginator = Paginator(wallets, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "wallets": wallets,
        "page_obj": page_obj
    }
    return render(request, "students/student_wallets.html", context)


@login_required(login_url="/users/login/")
def recharge_student_wallet(request: HttpRequest):
    if request.method == "POST":
        wallet_id = request.POST.get("wallet_id")
        recharge_method = request.POST.get("recharge_method")

        wallet = StudentWallet.objects.get(id=wallet_id)

        amount = Decimal(request.POST.get("amount"))

        wallet.balance += amount
        wallet.save()

        WalletRechargeLog.objects.create(
            student=wallet.student,
            wallet=wallet,
            recharge_method=recharge_method,
            amount_recharged=amount
        )
        return redirect("student-wallets")

    return render(request, "modals/request_recharge.html")


@login_required(login_url="/users/login/")
def generate_daily_quota(request: HttpRequest):
    student_wallets = StudentWallet.objects.filter(student__student_type="Boarder")

    if not student_wallets:
        print("Quotas for all students for today have been generated!!!")
        return redirect("student-wallets")

    for student_wallet in student_wallets:
        print(f"Student: {student_wallet.student}, Status: {student_wallet.student.status}, Student Type: {student_wallet.student.student_type}")
        student_wallet.total_spend_today = 0

        if student_wallet.student.status == "Deactivated":
            student_wallet.balance = 0
            student_wallet.save()
            student_wallet.student.credit_limit = 0
            student_wallet.student.save()
        else:
            student_wallet.balance = student_wallet.student.quota_group.amount
            student_wallet.save()
    # print(student_wallets)
    return redirect("student-wallets")