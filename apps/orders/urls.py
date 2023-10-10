from django.urls import path

from apps.orders.views import (add_to_cart, confirm_order, delete_order,
                               edit_order, edit_order_item, orders, pos,
                               pos_home, remove_from_cart,print_order_receipt)

urlpatterns = [
    path("", orders, name="orders"),
    path("edit-order/", edit_order, name="edit-order"),
    path("delete-order/", delete_order, name="delete-order"),

    path("pos-home/", pos_home, name="pos-home"),
    path("place-order/<int:student_id>/", pos, name="place-order"),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("confirm-order/", confirm_order, name="confirm-order"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove-from-cart"),
    path("edit-order-item/", edit_order_item, name="edit-order-item"),
    path("print-order/<int:order_id>/", print_order_receipt, name="print-order"),
]