from django.contrib import admin

from apps.inventory.models import Inventory, Menu, StockLog

# Register your models here.
admin.site.register(StockLog)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "item", "price"]

admin.site.register(Inventory)
