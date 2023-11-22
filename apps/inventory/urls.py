from django.urls import path

from apps.inventory.views import (delete_inventory_item, delete_menu_item,
                                  delete_supplier, edit_menu_item,
                                  edit_menu_item_amount, edit_supplier,
                                  inventory, menus, new_menu_item,
                                  new_stock_item, new_supplier, pay_supplier,
                                  re_stock, stock_logs, supplier_details,
                                  suppliers, take_out_stock)

urlpatterns = [
    path("", inventory, name="inventory"),
    path("delete-inventory/<int:id>/", delete_inventory_item, name="delete-inventory"),
    path("inventory-logs/", stock_logs, name="inventory-logs"),
    path("record-stock/", new_stock_item, name="record-stock"),
    path("re-stock/", re_stock, name="re-stock"),
    path("take-out/", take_out_stock, name="take-out"),
    path("pay-supplier/", pay_supplier, name="pay-supplier"),

    path("suppliers/", suppliers, name="suppliers"),
    path("suppliers/<int:supplier_id>/", supplier_details, name="supplier-details"),
    path("new-supplier/", new_supplier, name="new-supplier"),
    path("edit-supplier/", edit_supplier, name="edit-supplier"),
    path("delete-supplier/", delete_supplier, name="delete-supplier"),

    path("menus", menus, name="menus"),
    path("new-menu-item/", new_menu_item, name="new-menu-item"),
    path("edit-menu-item/", edit_menu_item, name="edit-menu-item"),
    path("delete-menu-item/", delete_menu_item, name="delete-menu-item"),
    path("edit-menu-item-amount/", edit_menu_item_amount, name="edit-menu-item-amount"),
]