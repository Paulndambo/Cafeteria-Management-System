from django.contrib import admin

from apps.students.models import Student


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display= ["registration_number", "status", "student_type"]


    