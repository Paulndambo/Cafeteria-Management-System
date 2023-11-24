from django.contrib import admin

from apps.reports.models import SalesReport


# Register your models here.
@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ["order", "amount"]