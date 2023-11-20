from django.urls import path

from apps.orders.views import (add_to_cart, clear_order_items, confirm_order,
                               confirm_overpaid_order,
                               decrease_order_item_quantity, delete_order,
                               edit_order, edit_order_item,
                               increase_order_item_quantity, orders, pos,
                               pos_home, print_order_receipt,
                               recharge_student_wallet_at_order,
                               remove_from_cart, void_customer_order)

urlpatterns = [
    path("", orders, name="orders"),
    path("edit-order/", edit_order, name="edit-order"),
    path("delete-order/", delete_order, name="delete-order"),

    path("recharge-wallet-at-order/", recharge_student_wallet_at_order, name="recharge-wallet-order"),

    path("pos-home/", pos_home, name="pos-home"),
    path("place-order/<int:student_id>/", pos, name="place-order"),
    path("add-to-cart/<int:menu_id>/<int:student_id>/", add_to_cart, name="add-to-cart"),
    path("confirm-order/<int:student_id>/", confirm_order, name="confirm-order"),
    path("confirm-manual-order/", confirm_overpaid_order, name="confirm-manual-order"),
    path("void-order/", void_customer_order, name="void-order"),
   
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove-from-cart"),
    path("clear-order-items/<int:student_id>/", clear_order_items, name="clear-order-items"),
    path("edit-order-item/", edit_order_item, name="edit-order-item"),
    path("print-order/<int:order_id>/", print_order_receipt, name="print-order"),
    path("increase-order-item-quantity/<int:item_id>/<int:student_id>/", increase_order_item_quantity, name="increase-order-item-quantity"),
    path("decrease-order-item-quantity/<int:item_id>/<int:student_id>/", decrease_order_item_quantity, name="decrease-order-item-quantity"),

    #path("customer-order/", customer_order, name="customer-order"),
    #path("add-cart-items/<int:item_id>/", add_cart_items, name="add-cart-items"),
    #path("delete-cart-item/<int:item_id>/", delete_cart_item, name="delete-cart-item"),
    #path("place-customer-mpesa-order/", place_customer_mpesa_order, name="place-customer-mpesa-order"),
    #path("place-customer-cash-order/", place_customer_cash_order, name="place-customer-cash-order"),
    #path("clear-shopping-cart/", clear_shopping_cart, name="clear-shopping-cart"),
    #path("increase-item-quantity/<int:item_id>/", increase_item_quantity, name="increase-item-quantity"),
    #path("decrease-item-quantity/<int:item_id>/", decrease_item_quantity, name="decrease-item-quantity"),
]