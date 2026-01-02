from django.urls import path

from apps.core.views import (delete_expense, edit_expense, expenses, home,
                             new_expense, quota_groups, new_quota_group, edit_quota_group,
                             export_expenses_csv)

urlpatterns = [
    path("", home, name="home"),
    path("expenses/", expenses, name="expenses"),
    path("new-expense/", new_expense, name="new-expense"),
    path("edit-expense/", edit_expense, name="edit-expense"),
    path("delete-expense/", delete_expense, name="delete-expense"),
    path("export-expenses-csv/", export_expenses_csv, name="export-expenses-csv"),
    path("quota-groups/", quota_groups, name="quota-groups"),
    path("new-quota-group/", new_quota_group, name="new-quota-group"),
    path("edit-quota-group/", edit_quota_group, name="edit-quota-group"),
]