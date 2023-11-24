from django.contrib import admin

from apps.orders.models import Order, OrderItem, TemporaryOrderItem


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["student", "total_cost", "payment_method"]

admin.site.register(TemporaryOrderItem)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "item", "quantity", "price"]