from django.urls import path

from apps.reports.views import daily_sales_data, today_sales_report, summary_stats, weekly_stats, daily_stats, monthly_stats

urlpatterns = [
    path("sales-today/", today_sales_report, name="sales-today"),
    path("daily-sales/", daily_sales_data, name="daily-sales"),
    path("summary-stats/", summary_stats, name="summary-stats"),
    path("weekly-stats/", weekly_stats, name="weekly-stats"),
    path("daily-stats/", daily_stats, name="daily-stats"),
    path("monthly-stats/", monthly_stats, name="monthly-stats"),
]