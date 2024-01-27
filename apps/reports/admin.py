from django.contrib import admin

from apps.reports.models import (DailySalesReport, GeneralisedReportData,
                                 SalesReport)


# Register your models here.
@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "order", "item", "quantity", "unit_price", "amount", "sold_or_spoiled"]

@admin.register(GeneralisedReportData)
class GeneralisedReportDataAdmin(admin.ModelAdmin):
    list_display = ["item", "quantity", "unit_price", "amount", "sold_or_spoiled"]


@admin.register(DailySalesReport)
class DailySalesReportAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "payment_method", "amount"]