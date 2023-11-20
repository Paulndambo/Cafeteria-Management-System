import csv
from datetime import datetime, timedelta

from django.shortcuts import render

# Create your views here.
from apps.reports.models import SalesReport


def today_sales_report(request):
    sales_today = SalesReport.objects.filter()
    context = {
        "sales_today": sales_today
    }
    return render(request, "reports/sales_today.html", context)