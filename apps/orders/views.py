from datetime import datetime
from decimal import Decimal

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.inventory.models import Menu
from apps.orders.models import Order, OrderItem, TemporaryOrderItem
from apps.students.models import Student, StudentWallet

date_today = datetime.now().date()
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
    quotas_generated = True

    boarding_student_wallets = StudentWallet.objects.filter(student__student_type="Boarder", student__status="Active").exclude(modified__date=date_today)

    print(f"Quotas Not Generated: {boarding_student_wallets.count()}")

    if boarding_student_wallets.count() >= 1:
        quotas_generated = False

    if request.method == "POST":
        id_number = request.POST.get("id_number")
        students = Student.objects.filter(Q(user__id_number__icontains=id_number) | Q(registration_number__icontains=id_number))

    context = {
        "students": students,
        "quotas_generated": quotas_generated
    }

    return render(request, "orders/pos_home.html", context)


def pos(request, student_id=None):
    student = Student.objects.get(id=student_id)
    menus = Menu.objects.all()#filter(added_to_cart=False)

    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")

        print(f"Name: {name}, Category: {category}")

        if name and category:
            menus = Menu.objects.filter(Q(item__icontains=name) | Q(category__icontains=category))
        elif name:
            menus = Menu.objects.filter(Q(item__icontains=name))
        elif category:
            menus = Menu.objects.filter(Q(category__icontains=category))

    items = TemporaryOrderItem.objects.filter(student=student)
    order_value = sum(TemporaryOrderItem.objects.filter(student=student).values_list("price", flat=True))

    menus = Menu.objects.exclude(
        id__in=list(TemporaryOrderItem.objects.filter(student=student).values_list('menu_item_id', flat=True))
    )

    extra_amount = order_value - student.studentwallet.balance 

    paginator = Paginator(menus, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "student": student,
        "menus": menus,
        "items": items,
        "page_obj": page_obj,
        "order_value": order_value,
        "extra_amount": extra_amount
    }
    return render(request, "orders/pos.html", context)

@transaction.atomic
def confirm_order(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        order_value = Decimal(request.POST.get("order_value"))
        student = Student.objects.get(id=student_id)
        meal_time = request.POST.get("meal_time")

        order = Order.objects.create(
            student=student,
            status="Processed",
            total_cost=order_value,
            meal_time=meal_time
        )

        items = TemporaryOrderItem.objects.all()

        order_items_list = []
        for order_item in items:
            order_items_list.append(OrderItem(
                order=order,
                item=order_item.menu_item,
                quantity=order_item.quantity,
                price=order_item.price
            ))

        order_items = OrderItem.objects.bulk_create(order_items_list)
        student.studentwallet.balance -= order_value
        student.studentwallet.save()
        Menu.objects.update(added_to_cart=False)
        TemporaryOrderItem.objects.all().delete()
        return redirect("orders")
    return render(request, "orders/confirm_order.html")


def add_to_cart(request):
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        student_id = request.POST.get("student_id")
        unit_price = Decimal(request.POST.get("price"))
        quantity = Decimal(request.POST.get("quantity"))

        menu_item = Menu.objects.get(id=menu_id)

        total_price = unit_price * quantity
        TemporaryOrderItem.objects.create(
            student_id=student_id,
            menu_item=menu_item,
            quantity=quantity,
            price=total_price
        )
        return redirect(f"/orders/place-order/{student_id}/")

    return render(request, "orders/add_to_cart.html")


def edit_order_item(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        order_item_id = request.POST.get("order_item_id")
        quantity = Decimal(request.POST.get("quantity"))

        item = TemporaryOrderItem.objects.get(id=order_item_id)
        item.quantity = quantity
        item.price = quantity * item.menu_item.price
        item.save()
        return redirect(f"/orders/place-order/{student_id}/")
    return render(request, "orders/edit_order_item.html")

def remove_from_cart(request, item_id=None):
    item = TemporaryOrderItem.objects.get(id=item_id)
    menu_item = Menu.objects.get(id=item.menu_item.id)
    menu_item.added_to_cart = False
    menu_item.save()

    student_id = item.student.id
    item.delete()
    return redirect(f"/orders/place-order/{student_id}/")


def print_order_receipt(request, order_id = None):
    order = Order.objects.get(id=order_id)
    order_items = order.orderitems.all()
    
    context = {
        "order": order,
        "order_items": order_items
    }
    return render(request, "orders/order_receipt.html", context)