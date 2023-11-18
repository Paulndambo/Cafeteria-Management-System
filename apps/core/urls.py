from django.urls import path

from apps.core.views import (delete_expense, edit_expense, expenses, home,
                             new_expense)

urlpatterns = [
    path("", home, name="home"),
    path("expenses/", expenses, name="expenses"),
    path("new-expense/", new_expense, name="new-expense"),
    path("edit-expense/", edit_expense, name="edit-expense"),
    path("delete-expense/", delete_expense, name="delete-expense"),
]