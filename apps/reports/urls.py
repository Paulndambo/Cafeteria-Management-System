from django.urls import path

from apps.reports.views import daily_sales_data, today_sales_report

urlpatterns = [
    path("sales-today/", today_sales_report, name="sales-today"),
    path("daily-sales/", daily_sales_data, name="daily-sales"),
]