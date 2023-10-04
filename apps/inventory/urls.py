from django.urls import path

from apps.inventory.views import inventory, new_stock_item, re_stock, take_out_stock

urlpatterns = [
    path("", inventory, name="inventory"),
    path("record-stock/", new_stock_item, name="record-stock"),
    path("re-stock/", re_stock, name="re-stock"),
    path("take-out/", take_out_stock, name="take-out"),
]