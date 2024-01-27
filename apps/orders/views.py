from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy

from apps.inventory.models import Menu
from apps.orders.models import (Order, OrderItem, TemporaryCustomerOrderItem,
                                TemporaryOrderItem)
from apps.reports.mixins import DailyReportMixin
from apps.reports.models import (DailySalesReport, GeneralisedReportData,
                                 SalesReport)
from apps.students.models import Student, StudentWallet, WalletRechargeLog

from .utils import determin_meal_time

date_today = datetime.now().date()
# Create your views here.


@login_required(login_url="/users/login/")
def orders(request):
    user = request.user
    orders = Order.objects.all().order_by("-created")

    if not user.is_superuser:
        orders = Order.objects.filter(served_by=user).order_by("-created")

    if request.method == "POST":
        registration_number = request.POST.get("reg_number")
        orders = Order.objects.filter(
            Q(student__registration_number__icontains=registration_number) | 
            Q(id__icontains=registration_number)
        )

    paginator = Paginator(orders, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": orders,
        "page_obj": page_obj,
    }
    return render(request, "orders/orders.html", context)


@login_required(login_url="/users/login/")
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


@login_required(login_url="/users/login/")
def delete_order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        order.delete()
        return redirect("orders")

    return render(request, "orders/delete_order.html")


@login_required(login_url="/users/login/")
def pos_home(request):
    students = Student.objects.none()
    students_list = Student.objects.all()
    quotas_generated = True

    boarding_student_wallets = StudentWallet.objects.filter(
        student__student_type="Boarder", student__status="Active").exclude(modified__date=date_today)

    print(f"Quotas Not Generated: {boarding_student_wallets.count()}")

    if boarding_student_wallets.count() >= 1:
        quotas_generated = False

    if request.method == "POST":
        id_number = request.POST.get("id_number")
        students = Student.objects.filter(Q(user__id_number__icontains=id_number) | Q(
            registration_number__icontains=id_number))

        if students.count() == 1:
            first_student = students.first()
            print(f"Student: {first_student.registration_number}")
            return redirect(f"/orders/place-order/{first_student.id}/")

    context = {
        "students": students,
        "quotas_generated": quotas_generated,
        "students_list": students_list
    }

    return render(request, "orders/pos_home.html", context)


@login_required(login_url="/users/login/")
def pos(request):
    user = request.user

    flag_irregularity = False
    is_walk_in_student = False

    menus_list = cache.get('menus')
    if not menus_list:
        test_menus = Menu.objects.all()
        cache.set('menus', test_menus, 3600)


    cashier_id = request.session.get("cashier_id")

    if not cashier_id:
        request.session["cashier_id"] = user.id

    students = Student.objects.all()
    menus = Menu.objects.none()  # filter(added_to_cart=False)
    selected_student = request.session.get(f'selected_student_{cashier_id}', {})

    quotas_generated = True

    boarding_student_wallets = StudentWallet.objects.filter(
        student__student_type="Boarder", student__status="Active").exclude(modified__date=date_today)

    print(f"Quotas Not Generated: {boarding_student_wallets.count()}")

    if boarding_student_wallets.count() >= 1:
        quotas_generated = False

    student = Student.objects.get(user__first_name='Walk-In')
    if not selected_student:
        request.session[f'selected_student_{cashier_id}'] = {
            'id': student.id,
            'last_name': student.user.last_name,
            'first_name': student.user.first_name,
            'registration_number': student.registration_number,
            'wallet_balance': str(student.wallet_balance),
            'cashier_id': cashier_id
        }
            
    print(f"Select Student: {selected_student}")

    context = {
        "selected_student": selected_student,
        "student": None,
        "menus": menus,
        "students": students,
        "quotas_generated": quotas_generated,
        "flag_irregularity": flag_irregularity
    }

    if selected_student:
        student = Student.objects.filter(
            id=selected_student['id']
        ).first()


        items = TemporaryOrderItem.objects.filter(student=student, user=user)
        order_value = sum(TemporaryOrderItem.objects.filter(
            student=student, user=user).values_list("price", flat=True))

        

        menus = menus_list.exclude(
            id__in=list(TemporaryOrderItem.objects.filter(
                student=student, user=user).values_list('menu_item_id', flat=True))
        ).filter(quantity__gt=0)

        extra_amount = order_value - student.studentwallet.balance

        student_orders = Order.objects.filter(student=student, created__date=date_today)

        if student.user.first_name == "Walk-In" and student.studentwallet.balance > 0:
            flag_irregularity = True
            is_walk_in_student = True

        if student.user.first_name == "Walk-In" and student.studentwallet.balance < 0:
            flag_irregularity = True
            is_walk_in_student = True

        elif student.user.first_name != "Walk-In":
            if student.studentwallet.balance > 350 or student.studentwallet.balance < 0:
                flag_irregularity = True
                

            elif student_orders:
                total_orders_today = 0

                total_orders_today = sum(list(student_orders.values_list("total_cost", flat=True)))

                if total_orders_today + student.studentwallet.balance > 350:
                    flag_irregularity = True
                else:
                    flag_irregularity = False
            elif student.studentwallet.balance > 350 or student.studentwallet.balance < 0:
                flag_irregularity = True


        if request.method == "POST":
            item = request.POST.get("item")
            print(f"Searched Item: {item}")
            menus = Menu.objects.filter(Q(item__icontains=item)).filter(quantity__gt=0)
            print(f"Found Menu Items: {menus}")
        

        context = {
            "student": student,
            "menus": menus,
            "items": items,
            #"page_obj": page_obj,
            "order_value": order_value,
            "extra_amount": extra_amount,
            "students": students,
            "selected_student": selected_student,
            "quotas_generated": quotas_generated,
            "flag_irregularity": flag_irregularity,
            "is_walk_in_student": is_walk_in_student
        }
    return render(request, "orders/pos.html", context)



@login_required(login_url="/users/login/")
@transaction.atomic
def confirm_order(request, student_id=None, *args, **kwargs):
    user = request.user
    cashier_id = request.session.get("cashier_id")
    student = Student.objects.get(id=student_id)
    meal_time = determin_meal_time()

    order_value = sum(TemporaryOrderItem.objects.filter(
        student=student, user=user).values_list("price", flat=True))

    order = Order.objects.create(
        student=student,
        status="Processed",
        total_cost=order_value,
        meal_time=meal_time,
        served_by=user,
        payment_method="Wallet"
    )

    items = TemporaryOrderItem.objects.filter(
        student=student,
        user=user
    )

    order_items_list = []
    for order_item in items:
        order_items_list.append(OrderItem(
            order=order,
            user=user,
            item=order_item.menu_item,
            quantity=order_item.quantity,
            price=order_item.price
        ))

    order_items = OrderItem.objects.bulk_create(order_items_list)

    for order_item in order_items:
        menu_item = Menu.objects.get(id=order_item.item.id)
        menu_item.quantity -= order_item.quantity
        menu_item.save()

     
        SalesReport.objects.create(
            order=order_item.order,
            item=menu_item.item,
            amount=menu_item.price * Decimal(order_item.quantity),
            sold_or_spoiled="Sold",
            quantity=order_item.quantity,
            unit_price=menu_item.price
        )

    DailySalesReport.objects.create(
        order=order,
        payment_method="Wallet",
        amount=order.total_cost
    )
    
    student.studentwallet.balance -= order_value
    student.studentwallet.total_spend_today += order_value
    student.studentwallet.save()

   

    Menu.objects.update(added_to_cart=False)
    TemporaryOrderItem.objects.filter(user=user, student=student).delete()
    del request.session[f'selected_student_{cashier_id}']
    return redirect(f"/orders/print-order/{order.id}/")


@login_required(login_url="/users/login/")
@transaction.atomic
def confirm_overpaid_order(request):
    user = request.user
    if request.method == "POST":
        recharge_method = request.POST.get("recharge_method")
        amount = Decimal(request.POST.get("amount"))
        student_id = int(request.POST.get("student_id"))

        student = Student.objects.get(id=student_id)

        recharge_log = WalletRechargeLog.objects.create(
            student=student,
            wallet=student.studentwallet,
            recharge_method=recharge_method,
            amount_recharged=amount
        )

        student.studentwallet.balance += amount
        student.studentwallet.save()


        meal_time = determin_meal_time()

        order_value = sum(TemporaryOrderItem.objects.filter(
            student=student, user=user).values_list("price", flat=True))

        if recharge_method.lower() == "cash":
            order = Order.objects.create(
                student=student,
                status="Processed",
                total_cost=order_value,
                meal_time=meal_time,
                served_by=user, 
                payment_method="Wallet And Cash"
            )
        elif recharge_method.lower() == "mpesa":
            order = Order.objects.create(
                student=student,
                status="Processed",
                total_cost=order_value,
                meal_time=meal_time,
                served_by=user, 
                payment_method="Wallet And Mpesa"
            )
        else:
            print(f"Recharge Method: {recharge_method} Was not found")

        items = TemporaryOrderItem.objects.filter(
            user=user,
            student=student
        )

        order_items_list = []
        for order_item in items:
            order_items_list.append(OrderItem(
                order=order,
                user=user,
                item=order_item.menu_item,
                quantity=order_item.quantity,
                price=order_item.price
            ))

        order_items = OrderItem.objects.bulk_create(order_items_list)

        for order_item in order_items:
            menu_item = Menu.objects.get(id=order_item.item.id)
            menu_item.quantity -= order_item.quantity
            menu_item.save()
            
            SalesReport.objects.create(
                order=order_item.order,
                item=menu_item.item,
                amount=menu_item.price * Decimal(order_item.quantity),
                sold_or_spoiled="Sold",
                quantity=order_item.quantity,
                unit_price=menu_item.price
            )

        mixin = DailyReportMixin(
            order=order,
            recharge_method=recharge_method,
            order_value=order_value,
            amount=amount
        )
        mixin.run()

        student.studentwallet.balance -= order_value
        student.studentwallet.total_spend_today += order_value
        student.studentwallet.save()

        
        Menu.objects.update(added_to_cart=False)
        TemporaryOrderItem.objects.filter(user=user, student=student).delete()
        return redirect(f"/orders/print-order/{order.id}/")


@login_required(login_url="/users/login/")
def add_to_cart(request, menu_id=None, student_id=None):
    user = request.user
    menu_item = Menu.objects.get(id=menu_id)

    item_check = TemporaryOrderItem.objects.filter(
        student_id=student_id,
        menu_item=menu_item,
        user=user
    ).first()

    total_price = menu_item.price * 1
    if item_check:
        item_check.quantity += 1
        item_check.price += total_price
        item_check.save()
    else:
        TemporaryOrderItem.objects.create(
            user=user,
            student_id=student_id,
            menu_item=menu_item,
            quantity=1,
            price=total_price
        )
    return redirect(f"/orders/place-order/")


@login_required(login_url="/users/login/")
def edit_order_item(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        order_item_id = request.POST.get("order_item_id")
        quantity = Decimal(request.POST.get("quantity"))

        item = TemporaryOrderItem.objects.get(id=order_item_id, student_id=student_id)
        item.quantity = quantity
        item.price = quantity * item.menu_item.price
        item.save()
        return redirect(f"/orders/place-order/{student_id}/")
    return render(request, "orders/edit_order_item.html")


@login_required(login_url="/users/login/")
def remove_from_cart(request, item_id=None, student_id=None):
    item = TemporaryOrderItem.objects.get(id=item_id)
    menu_item = Menu.objects.get(id=item.menu_item.id)
    menu_item.added_to_cart = False
    menu_item.save()

    student_id = item.student.id
    item.delete()
    return redirect(f"/orders/place-order/")


@login_required(login_url="/users/login/")
def print_order_receipt(request, order_id=None):
    user = request.user
    cashier_id = request.session.get("cashier_id")
    order = Order.objects.get(id=order_id)
    order_items = order.orderitems.all()

    context = {
        "order": order,
        "order_items": order_items
    }
    if request.session.get(f'selected_student_{cashier_id}'):
        del request.session[f'selected_student_{cashier_id}']
    return render(request, "orders/receipt.html", context)


@login_required(login_url="/users/login/")
def increase_order_item_quantity(request, item_id=None, student_id=None):
    item = TemporaryOrderItem.objects.get(id=item_id, student_id=student_id)
    item.quantity += 1
    item.price += item.menu_item.price
    item.save()
    print(f"Student ID: {student_id}")
    return redirect(f"/orders/place-order/")


@login_required(login_url="/users/login/")
def decrease_order_item_quantity(request, item_id=None, student_id=None):
    item = TemporaryOrderItem.objects.get(id=item_id, student_id=student_id)
    if item.quantity == 0:
        item.quantity = 0
        item.save()
    else:
        item.quantity -= 1
        item.price -= item.menu_item.price
        item.save()
    return redirect(f"/orders/place-order/")


@login_required(login_url="/users/login/")
def clear_order_items(request, student_id=None):
    items = TemporaryOrderItem.objects.filter(student_id=student_id)
    if items:
        items.delete()
        print(items)
    return redirect(f"/orders/place-order/")


@login_required(login_url="/users/login/")
def recharge_student_wallet_at_order(request):
    cashier_id = request.session.get("cashier_id")
    if request.method == "POST":
        reg_number = request.POST.get("reg_number")
        recharge_method = request.POST.get("recharge_method")

        student = Student.objects.filter(
            Q(registration_number=reg_number) | Q(user__id_number=reg_number)).first()

        amount = Decimal(request.POST.get("amount"))

        wallet = student.studentwallet
        wallet.balance += amount
        wallet.save()

        recharge_log = WalletRechargeLog.objects.create(
            student=student,
            wallet=wallet,
            recharge_method=recharge_method,
            amount_recharged=amount
        )
        del request.session[f'selected_student_{cashier_id}']
        return redirect(f"/orders/place-order/{student.id}")

    return render(request, "modals/request_recharge.html")


@transaction.atomic
def void_customer_order(request):
    if request.method == "POST":
        order_id = int(request.POST.get("order_id"))

        order = Order.objects.get(id=order_id)
        order.status = "Nullified"
        order.total_cost = 0

        order_items = order.orderitems.all()

        for order_item in order_items:
            menu = Menu.objects.get(id=order_item.item.id)
            menu.quantity += order_item.quantity
            menu.save()

        
        daily_sales_reports = DailySalesReport.objects.filter(order=order)
        
        for sale_report in daily_sales_reports:
            if sale_report.payment_method in ["Mpesa", "Cash"]:
                sale_report.amount = 0
                sale_report.save()

            elif sale_report.payment_method == "Wallet":
                student = sale_report.order.student
                student_wallet = student.studentwallet
                student_wallet.balance += sale_report.amount
                student_wallet.total_spend_today -= sale_report.amount
                student_wallet.save()

                sale_report.amount = 0
                sale_report.save()

        daily_sales_reports.delete()
        sales_reports = SalesReport.objects.filter(order=order)
        sales_reports.delete()
        order_items.delete()


        order.save()

        return redirect("orders")
    return render(request, "orders/void_order.html")


@login_required(login_url="/users/login/")
def clear_student_from_pos(request):
    cashier_id = request.session.get("cashier_id")
    del request.session[f'selected_student_{cashier_id}']
    return redirect("place-order")