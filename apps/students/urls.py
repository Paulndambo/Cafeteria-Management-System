from django.urls import path

from apps.students.views import (
    students, new_student, student_wallets, recharge_student_wallet, 
    delete_student, edit_student
)

urlpatterns = [
    path("", students, name="students"),
    path("new-student/", new_student, name="new-student"),
    path("delete-student/", delete_student, name="delete-student"),
    path("edit-student/", edit_student, name="edit-student"),
    path("student-wallets/", student_wallets, name="student-wallets"),
    path("recharge-wallet/<int:student_id>/", recharge_student_wallet, name="recharge-wallet"),
]