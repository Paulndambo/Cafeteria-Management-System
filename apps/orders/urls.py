from django.urls import path

from apps.orders.views import delete_order, edit_order, orders, pos_home

urlpatterns = [
    path("", orders, name="orders"),
    path("edit-order/", edit_order, name="edit-order"),
    path("delete-order/", delete_order, name="delete-order"),

    path("pos-home/", pos_home, name="pos-home"),
]