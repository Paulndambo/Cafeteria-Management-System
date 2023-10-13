from django.contrib import admin

from apps.inventory.models import Inventory, Menu, StockLog

# Register your models here.
admin.site.register(StockLog)
admin.site.register(Menu)
admin.site.register(Inventory)
