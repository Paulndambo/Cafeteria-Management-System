from django.contrib import admin
from apps.students.models import Student, StudentWallet
# Register your models here.
admin.site.register(Student)
admin.site.register(StudentWallet)