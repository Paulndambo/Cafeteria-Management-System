from django.urls import path
from apps.reports.views import today_sales_report

urlpatterns = [
    path("sales-today/", today_sales_report, name="sales-today"),
]