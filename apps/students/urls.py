from django.urls import path

from apps.students.views import students, new_student, student_wallets

urlpatterns = [
    path("", students, name="students"),
    path("new-student/", new_student, name="new-student"),
    path("student-wallets/", student_wallets, name="student-wallets"),
]