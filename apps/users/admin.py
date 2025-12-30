from django.contrib import admin
from apps.users.models import User
# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
 