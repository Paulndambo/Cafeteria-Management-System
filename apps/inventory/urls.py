from django.urls import path

from apps.inventory.views import inventory, new_stock_item

urlpatterns = [
    path("", inventory, name="inventory"),
    path("record-stock/", new_stock_item, name="record-stock"),
]