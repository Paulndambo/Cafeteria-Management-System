from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from apps.core.models import Expense
from apps.orders.models import Order
from apps.reports.models import SalesReport
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
        purpose = request.POST.get("purpose")
        amount = Decimal(request.POST.get("amount"))

        expense = Expense.objects.create(
            title=title,
            purpose=purpose,
            amount=amount
        )
        return redirect("expenses")

    return render(request, "expenses/new_expense.html")


def edit_expense(request):
    if request.method == "POST":
        expense_id = int(request.POST.get("expense_id"))
        title = request.POST.get("title")
        purpose = request.POST.get("purpose")
        amount = Decimal(request.POST.get("amount"))

        expense = Expense.objects.get(id=expense_id)
        expense.title = title
        expense.purpose = purpose
        expense.amount = amount
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
    students = Student.objects.count()
    staffs = User.objects.filter(role__in=["chef", "admin", "cashier"]).count()
    orders_today = Order.objects.filter(created__date=date_today).count()

    ### Data Today
    mpesa_sales_today = sum(list(SalesReport.objects.filter(
        created__date=date_today, 
        payment_method="Mpesa"
    ).values_list("amount", flat=True)))

    cash_sales_today = sum(list(SalesReport.objects.filter(
        created__date=date_today, 
        payment_method="Cash"
    ).values_list("amount", flat=True)))

    wallet_sales_today = sum(list(SalesReport.objects.filter(
        created__date=date_today, 
        payment_method="Wallet"
    ).values_list("amount", flat=True)))

    ### Data This Week
    mpesa_sales_this_month = sum(list(SalesReport.objects.filter(
        created__month=date_today.month, 
        payment_method="Mpesa"
    ).values_list("amount", flat=True)))

    wallet_sales_this_month = sum(list(SalesReport.objects.filter(
        created__month=date_today.month, 
        payment_method="Wallet"
    ).values_list("amount", flat=True)))

    cash_sales_this_month = sum(list(SalesReport.objects.filter(
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
        "wallet_sales_this_month": wallet_sales_this_month
    }
    return render(request, "home.html", context)