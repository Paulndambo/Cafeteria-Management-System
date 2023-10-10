from datetime import datetime

from django.shortcuts import render

from apps.orders.models import Order
from apps.students.models import Student, StudentWallet
from apps.users.models import User

date_today = datetime.now().date()
# Create your views here.
def home(request):
    students = Student.objects.count()
    staffs = User.objects.filter(role="admin").count()
    orders_today = Order.objects.filter(created__date=date_today).count()

    context = {
        "students": students,
        "staffs": staffs,
        "orders_today": orders_today
    }
    return render(request, "home.html", context)