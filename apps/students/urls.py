from django.urls import path

from apps.students.views import (activate_deactivate_student, delete_student,
                                 edit_student,
                                 new_student,
                                 search_student, student_details,
                                 students, students_finder,
                                 turn_balance_to_zero, upload_students)

urlpatterns = [
    path("", students, name="students"),
    path("new-student/", new_student, name="new-student"),
    path("activate-deactivate-student/<int:student_id>/", activate_deactivate_student, name="activate-deactivate-student"),
    path("delete-student/", delete_student, name="delete-student"),
    path("edit-student/", edit_student, name="edit-student"),
    path("upload-students/", upload_students, name="upload-students"),
    path("students-finder/", students_finder, name="students-finder"),
    path("students/<int:student_id>/", student_details, name="student-details"),
    path("search-student/", search_student, name="search-student"),
    path("set-zero-balance/<int:student_id>/", turn_balance_to_zero, name="set-zero-balance"),
]