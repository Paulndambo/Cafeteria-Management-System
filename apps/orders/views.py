from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.orders.models import Order, OrderItem
from apps.students.models import Student


# Create your views here.
def orders(request):
    orders = Order.objects.all()
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": orders,
        "page_obj": page_obj,
    }
    return render(request, "orders/orders.html", context)


def edit_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        status = request.POST.get("status")
        meal_time = request.POST.get("meal_time")
       

        order = Order.objects.get(id=order_id)
        order.status = status
        order.meal_time = meal_time
        order.save()
        return redirect("orders")

    return render(request, "orders/edit_order.html")


def delete_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        order.delete()
        return redirect("orders")
        
    return render(request, "orders/delete_order.html")


def pos_home(request):
    students = Student.objects.none()

    if request.method == "POST":
        id_number = request.POST.get("id_number")
        students = Student.objects.filter(Q(user__id_number=id_number) | Q(registration_number=id_number))

    context = {
        "students": students
    }

    return render(request, "orders/pos_home.html", context)