from django.urls import path

from apps.inventory.views import (delete_supplier, edit_supplier, inventory,
                                  new_stock_item, new_supplier, re_stock,
                                  stock_logs, suppliers, take_out_stock)

urlpatterns = [
    path("", inventory, name="inventory"),
    path("inventory-logs/", stock_logs, name="inventory-logs"),
    path("record-stock/", new_stock_item, name="record-stock"),
    path("re-stock/", re_stock, name="re-stock"),
    path("take-out/", take_out_stock, name="take-out"),

    path("suppliers/", suppliers, name="suppliers"),
    path("new-supplier/", new_supplier, name="new-supplier"),
    path("edit-supplier/", edit_supplier, name="edit-supplier"),
    path("delete-supplier/", delete_supplier, name="delete-supplier"),
]