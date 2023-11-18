from django.urls import path

from apps.students.views import (activate_deactivate_student, delete_student,
                                 edit_student, generate_daily_quota,
                                 new_student, recharge_student_wallet,
                                 student_wallets, students, upload_students)

urlpatterns = [
    path("", students, name="students"),
    path("new-student/", new_student, name="new-student"),
    path("activate-deactivate-student/<int:student_id>/", activate_deactivate_student, name="activate-deactivate-student"),
    path("delete-student/", delete_student, name="delete-student"),
    path("edit-student/", edit_student, name="edit-student"),
    path("student-wallets/", student_wallets, name="student-wallets"),
    path("recharge-wallet/", recharge_student_wallet, name="recharge-wallet"),
    path("generate-daily-quotas/", generate_daily_quota, name="generate-daily-quotas"),
    path("upload-students/", upload_students, name="upload-students"),
]