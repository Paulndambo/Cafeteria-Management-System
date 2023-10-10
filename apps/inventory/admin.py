from django.contrib import admin

from apps.inventory.models import Menu, StockLog

# Register your models here.
admin.site.register(StockLog)
admin.site.register(Menu)
