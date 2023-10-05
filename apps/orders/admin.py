from django.contrib import admin

from apps.orders.models import Order, TemporaryOrderItem

# Register your models here.
admin.site.register(Order)
admin.site.register(TemporaryOrderItem)