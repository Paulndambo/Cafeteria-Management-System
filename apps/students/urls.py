from django.urls import path

from apps.students.views import (activate_deactivate_student, delete_student,
                                 edit_student, new_student,
                                 recharge_student_wallet, student_wallets,
                                 students)

urlpatterns = [
    path("", students, name="students"),
    path("new-student/", new_student, name="new-student"),
    path("activate-deactivate-student/<int:student_id>/", activate_deactivate_student, name="activate-deactivate-student"),
    path("delete-student/", delete_student, name="delete-student"),
    path("edit-student/", edit_student, name="edit-student"),
    path("student-wallets/", student_wallets, name="student-wallets"),
    path("recharge-wallet/<int:student_id>/", recharge_student_wallet, name="recharge-wallet"),
]