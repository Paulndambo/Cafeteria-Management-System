from datetime import datetime, timedelta
from decimal import Decimal
import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.core.models import Expense, QuotaGroup
from apps.orders.models import Order
from apps.reports.models import DailySalesReport
from apps.students.models import Student
from apps.wallets.models import StudentWallet
from apps.users.models import User
from apps.core.constants import get_month_name, format_date

date_today = datetime.now().date()
# Create your views here.
def expenses(request):
    expenses = Expense.objects.all().order_by('-expense_date')
    
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Apply date filters if provided
    if start_date:
        expenses = expenses.filter(expense_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(expense_date__lte=end_date)
    
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "expenses": expenses,
        "page_obj": page_obj,
        "payment_methods": ["Mpesa", "Cash"],
        "start_date": start_date or '',
        "end_date": end_date or '',
    }

    return render(request, "expenses/expenses.html", context)

def new_expense(request):
    if request.method == "POST":
        title = request.POST.get("title")
        payment_method = request.POST.get("payment_method")
        expense_date = request.POST.get("expense_date")
        amount = Decimal(request.POST.get("amount"))

        expense_date_formatted = format_date(expense_date)
        month_name = get_month_name(expense_date_formatted.month)

        Expense.objects.create(
            title=title,
            month=month_name,
            year=str(expense_date_formatted.year),
            expense_date=expense_date_formatted,
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
        expense_date = request.POST.get("expense_date")
        amount = Decimal(request.POST.get("amount"))

        formatted_expense_date = format_date(expense_date)
        month_name = get_month_name(formatted_expense_date.month)

        Expense.objects.filter(id=expense_id).update(
            title=title,
            expense_date=formatted_expense_date,
            month=month_name,
            year=str(formatted_expense_date.year),
            amount=amount,
            payment_method=payment_method
        )

        return redirect("expenses")
    return render(request, "expenses/edit_expense.html")


def delete_expense(request):
    if request.method == "POST":
        expense_id = int(request.POST.get("expense_id"))

        expense = Expense.objects.get(id=expense_id)
        expense.delete()

        return redirect("expenses")
    return render(request, "expenses/delete_expense.html")


def export_expenses_csv(request):
    """Export expenses to CSV file with optional date filtering"""
    expenses = Expense.objects.all().order_by('-expense_date')
    
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Apply date filters if provided
    if start_date:
        expenses = expenses.filter(expense_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(expense_date__lte=end_date)
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    
    # Generate filename with date range if applicable
    if start_date and end_date:
        filename = f'Expenses_{start_date}_to_{end_date}.csv'
    elif start_date:
        filename = f'Expenses_from_{start_date}.csv'
    elif end_date:
        filename = f'Expenses_until_{end_date}.csv'
    else:
        filename = f'Expenses_{date_today}.csv'
    
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['ID', 'Expense Name', 'Amount', 'Payment Method', 'Date', 'Month', 'Year'])
    
    # Write data rows
    for expense in expenses:
        writer.writerow([
            expense.id,
            expense.title,
            expense.amount,
            expense.payment_method,
            expense.expense_date,
            expense.month,
            expense.year
        ])
    
    return response


@login_required(login_url="/users/login/")
def home(request):
    user = request.user

    if user.role == "chef":
        return redirect("menus")

    elif user.role == "cashier":
        return redirect("place-order")

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


def quota_groups(request):
    quota_groups = QuotaGroup.objects.all()
    

    context = {
        "groups": quota_groups,
        "student_types": ["Prepaid", "Boarder", "One-Time"]
    }

    return render(request, "quotas/groups.html", context)


def new_quota_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = Decimal(request.POST.get("amount"))
        student_type = request.POST.get("student_type")

        QuotaGroup.objects.create(
            name=name,
            amount=amount,
            student_type=student_type
        )
        return redirect("quota-groups")

    return render(request, "quotas/new_group.html")


def edit_quota_group(request):
    if request.method == "POST":
        quota_group_id = int(request.POST.get("group_id"))
        name = request.POST.get("name")
        amount = Decimal(request.POST.get("amount"))
        student_type = request.POST.get("student_type")

        quota_group = QuotaGroup.objects.get(id=quota_group_id)
        quota_group.name = name
        quota_group.amount = amount
        quota_group.student_type = student_type
        quota_group.save()
        

        return redirect("quota-groups")
    return render(request, "quotas/edit_group.html")