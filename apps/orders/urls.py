from django.urls import path

from apps.orders.views import (add_cart_items, add_to_cart,
                               clear_shopping_cart, confirm_order,
                               customer_order, decrease_item_quantity,
                               decrease_order_item_quantity, delete_cart_item,
                               delete_order, edit_order, edit_order_item,
                               increase_item_quantity,
                               increase_order_item_quantity, orders,
                               place_customer_order, pos, pos_home,
                               print_order_receipt, remove_from_cart)

urlpatterns = [
    path("", orders, name="orders"),
    path("edit-order/", edit_order, name="edit-order"),
    path("delete-order/", delete_order, name="delete-order"),

    path("pos-home/", pos_home, name="pos-home"),
    path("place-order/<int:student_id>/", pos, name="place-order"),
    path("add-to-cart/<int:menu_id>/<int:student_id>/", add_to_cart, name="add-to-cart"),
    path("confirm-order/<int:student_id>/", confirm_order, name="confirm-order"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove-from-cart"),
    path("edit-order-item/", edit_order_item, name="edit-order-item"),
    path("print-order/<int:order_id>/", print_order_receipt, name="print-order"),
    path("increase-order-item-quantity/<int:item_id>/<int:student_id>/", increase_order_item_quantity, name="increase-order-item-quantity"),
    path("decrease-order-item-quantity/<int:item_id>/<int:student_id>/", decrease_order_item_quantity, name="decrease-order-item-quantity"),

    path("customer-order/", customer_order, name="customer-order"),
    path("add-cart-items/<int:item_id>/", add_cart_items, name="add-cart-items"),
    path("delete-cart-item/<int:item_id>/", delete_cart_item, name="delete-cart-item"),
    path("place-customer-order/", place_customer_order, name="place-customer-order"),
    path("clear-shopping-cart/", clear_shopping_cart, name="clear-shopping-cart"),
    path("increase-item-quantity/<int:item_id>/", increase_item_quantity, name="increase-item-quantity"),
    path("decrease-item-quantity/<int:item_id>/", decrease_item_quantity, name="decrease-item-quantity"),
]