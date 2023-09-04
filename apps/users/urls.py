from django.urls import path
from apps.users.views import (
    user_login, user_logout, register, staff
)


urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("logout/", user_logout, name="logout"),
    path("staff/", staff, name="staff"),
]