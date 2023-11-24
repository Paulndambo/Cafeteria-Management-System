from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.core.models import Expense
from apps.orders.models import Order
from apps.reports.models import DailySalesReport
from apps.students.models import Student, StudentWallet
from apps.users.models import User

date_today = datetime.now().date()
# Create your views here.
def expenses(request):
    expenses = Expense.objects.all()
    
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "expenses": expenses,
        "page_obj": page_obj
    }

    return render(request, "expenses/expenses.html", context)

def new_expense(request):
    if request.method == "POST":
        title = request.POST.get("title")
        payment_method = request.POST.get("payment_method")
        purpose = request.POST.get("purpose")
        amount = Decimal(request.POST.get("amount"))

        expense = Expense.objects.create(
            title=title,
            purpose=purpose,
            amount=amount,
            payment_method=payment_method
        )
        return redirect("expenses")

    return render(request, "expenses/new_expense.html")


def edit_expense(request):
    if request.method == "POST":
        expense_id = int(request.POST.get("expense_id"))
        title = request.POST.get("title")
        payment_method = request.POST.get("payment_method")
        purpose = request.POST.get("purpose")
        amount = Decimal(request.POST.get("amount"))

        expense = Expense.objects.get(id=expense_id)
        expense.title = title
        expense.purpose = purpose
        expense.amount = amount
        expense.payment_method = payment_method
        expense.save()
        

        return redirect("expenses")
    return render(request, "expenses/edit_expense.html")


def delete_expense(request):
    if request.method == "POST":
        expense_id = int(request.POST.get("expense_id"))

        expense = Expense.objects.get(id=expense_id)
        expense.delete()

        return redirect("expenses")
    return render(request, "expenses/delete_expense.html")


@login_required(login_url="/users/login/")
def home(request):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=6)

    students = Student.objects.count()
    staffs = User.objects.filter(role__in=["chef", "admin", "cashier"]).count()
    orders_today = Order.objects.filter(created__date=date_today).count()

    ### Data Today
    mpesa_sales_today = sum(list(DailySalesReport.objects.filter(
        created__date=date_today, 
        payment_method="Mpesa"
    ).values_list("amount", flat=True)))

    cash_sales_today = sum(list(DailySalesReport.objects.filter(
        created__date=date_today, 
        payment_method="Cash"
    ).values_list("amount", flat=True)))

    wallet_sales_today = sum(list(DailySalesReport.objects.filter(
        created__date=date_today, 
        payment_method="Wallet"
    ).values_list("amount", flat=True)))

    ### Data this week
    mpesa_sales_this_week = sum(list(DailySalesReport.objects.filter(
        created__range=[start_date, end_date], payment_method="Mpesa"
    ).values_list("amount", flat=True)))
    wallet_sales_this_week = sum(list(DailySalesReport.objects.filter(
        created__range=[start_date, end_date], payment_method="Wallet"
    ).values_list("amount", flat=True)))
    cash_sales_this_week = sum(list(DailySalesReport.objects.filter(
        created__range=[start_date, end_date], payment_method="Cash"
    ).values_list("amount", flat=True)))

    print("Mpesa: ", mpesa_sales_this_week)
    print("Cash: ", cash_sales_this_week)
    print("Wallet: ", wallet_sales_this_week)
    ### Data This Month
    mpesa_sales_this_month = sum(list(DailySalesReport.objects.filter(
        created__month=date_today.month, 
        payment_method="Mpesa"
    ).values_list("amount", flat=True)))

    wallet_sales_this_month = sum(list(DailySalesReport.objects.filter(
        created__month=date_today.month, 
        payment_method="Wallet"
    ).values_list("amount", flat=True)))

    cash_sales_this_month = sum(list(DailySalesReport.objects.filter(
        created__month=date_today.month, 
        payment_method="Cash"
    ).values_list("amount", flat=True)))

    context = {
        "students": students,
        "staffs": staffs,
        "orders_today": orders_today,
        "mpesa_sales_today": mpesa_sales_today,
        "wallet_sales_today": wallet_sales_today,
        "cash_sales_today": cash_sales_today,
        "mpesa_sales_this_month": mpesa_sales_this_month,
        "cash_sales_this_month": cash_sales_this_month,
        "wallet_sales_this_month": wallet_sales_this_month,
        "wallet_sales_this_week": wallet_sales_this_week,
        "cash_sales_this_week": cash_sales_this_week,
        "mpesa_sales_this_week": mpesa_sales_this_week
    }
    return render(request, "home.html", context)