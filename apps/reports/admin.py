from django.contrib import admin

from apps.reports.models import SalesReport, GeneralisedReportData


# Register your models here.
@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ["order", "amount"]

@admin.register(GeneralisedReportData)
class GeneralisedReportDataAdmin(admin.ModelAdmin):
    list_display = ["item", "quantity", "unit_price", "amount", "sold_or_spoiled"]