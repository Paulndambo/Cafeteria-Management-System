from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.core.models import Expense
from apps.inventory.models import (Inventory, Menu, StockLog, Supplier,
                                   SupplyLog)

date_today = datetime.now().date()
# Create your views here.
def menus(request):
    menus = Menu.objects.all()
    paginator = Paginator(menus, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "menus": menus,
        "page_obj": page_obj,
        "date_today": date_today
    }
    return render(request, "menus/menu.html", context)


def new_menu_item(request):
    if request.method == "POST":
        item = request.POST.get("item")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.FILES["image"]

        menu = Menu.objects.create(
            item=item,
            price=price,
            quantity=quantity,
            image=image,
            starting_stock=quantity
        )

        return redirect("menus")
    return render(request, "menus/new_menu_item.html")


def edit_menu_item(request):
    if request.method == "POST":
        menu_id = int(request.POST.get("menu_id"))
        item = request.POST.get("item")
        price = Decimal(request.POST.get("price"))
        image = request.FILES["image"]
    
        quantity = float(request.POST.get("quantity"))
        

        menu_item = Menu.objects.get(id=menu_id)
        menu_item.item = item
        menu_item.price = price
        menu_item.quantity = quantity
        menu_item.starting_stock = quantity
        menu_item.image = image
        menu_item.updated_today = date_today
        menu_item.save()

        return redirect("menus")

    return render(request, "menus/edit_menu.html")

def edit_menu_item_amount(request):
    if request.method == "POST":
        menu_id = int(request.POST.get("menu_id"))
        quantity = float(request.POST.get("quantity"))
        
        menu_item = Menu.objects.get(id=menu_id)
        menu_item.quantity += quantity
        menu_item.starting_stock += quantity
        menu_item.save()

        return redirect("menus")

    return render(request, "menus/edit_menu_item.html")


def delete_menu_item(request):
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        menu_item = Menu.objects.get(id=menu_id)
        menu_item.delete()
        return redirect("menus")

    return render(request, "menus/delete_menu.html")


@login_required(login_url="/users/login/")
def suppliers(request):
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        suppliers = Supplier.objects.filter(Q(name__icontains=name))

    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stock_items": suppliers,
        "page_obj": page_obj,
    }
    return render(request, "suppliers/suppliers.html", context)


def supplier_details(request, supplier_id=None):
    supplier = Supplier.objects.get(id=supplier_id)
    supplies = supplier.mysupplies.all()

    paginator = Paginator(supplies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "supplier": supplier,
        "supplies": supplies,
        "page_obj": page_obj
    }
    return render(request, "suppliers/supplier_details.html", context)

@login_required(login_url="/users/login/")
def delete_supplier(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier_id")
        student = Supplier.objects.filter(id=supplier_id).first()
        if student:
            student.delete()
            return redirect("suppliers")
        else:
            return messages.error(request, f"Student with id: {supplier_id} does not exist on the database")
    return render(request, "modals/students/delete_student.html")


@login_required(login_url="/users/login/")
def new_supplier(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        postal_address = request.POST.get("postal_address")
        town = request.POST.get("town")
        country = request.POST.get("country")

        supplier = Supplier.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
            postal_address=postal_address,
            town=town,
            country=country
        )


        return redirect("suppliers")

    return render(request, "suppliers/edit_supplier.html")


@login_required(login_url="/users/login/")
def edit_supplier(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        postal_address = request.POST.get("postal_address")
        town = request.POST.get("town")
        country = request.POST.get("country")

        supplier = Supplier.objects.get(id=supplier_id)
        supplier.name = name if name else supplier.name
        supplier.email = email if email else supplier.email
        supplier.phone_number = phone_number if phone_number else supplier.phone_number
        supplier.postal_address = postal_address if postal_address else supplier.postal_address
        supplier.town = town if town else supplier.town
        supplier.country = country if country else supplier.country
        supplier.save()

        return redirect("suppliers")

    return render(request, "suppliers/edit_supplier.html")


@login_required(login_url="/users/login/")
def inventory(request):
    stock_items = Inventory.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        stock_items = Inventory.objects.filter(Q(name__icontains=name))

    paginator = Paginator(stock_items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stock_items": stock_items,
        "page_obj": page_obj,
        "suppliers": suppliers
    }
    return render(request, "inventory/inventory.html", context)


@login_required(login_url="/users/login/")
def delete_inventory_item(request, id=None):
    item = Inventory.objects.get(id=id)
    item.delete()
    return redirect("inventory")


@login_required(login_url="/users/login/")
def new_stock_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        payment_method = request.POST.get("payment_method")
        unit = request.POST.get("unit")
        unit_price = Decimal(request.POST.get("unit_price"))
        #selling_price = Decimal(request.POST.get("selling_price"))
        stock = Decimal(request.POST.get("stock"))
        supplier_id = int(request.POST.get("supplier_id"))

        supplier = Supplier.objects.get(id=supplier_id)
        supply_cost = unit_price * Decimal(stock)

        print(f"Type of Total Supplies Cost: {type(supplier.total_supplies_cost)}")
        print(f"Type of Supply Cost: {type(supply_cost)}")


        if payment_method == "Credit":
            supplier.amount_owed += supply_cost
        elif payment_method in ["Mpesa", "Cash"]:

            supplier.total_paid += supply_cost
        supplier.total_supplies_cost += supply_cost

        supplier.save()

        inventory = Inventory.objects.create(
            supplier=supplier,
            name=name,
            unit_price=unit_price,
            unit=unit,
            stock=stock,
            payment_method=payment_method,
        )

        if payment_method == "Credit":
            supply_log = SupplyLog.objects.create(
                supplier=supplier,
                item=name,
                quantity_supplied=stock,
                unit_price=unit_price,
                payment_method=payment_method,
                total_cost = supply_cost,
                supply_unit=unit,
                amount_due=supply_cost,
                amount_paid=0
            )
        elif payment_method in ["Cash", "Mpesa"]:
            supply_log = SupplyLog.objects.create(
                supplier=supplier,
                item=name,
                quantity_supplied=stock,
                unit_price=unit_price,
                payment_method=payment_method,
                total_cost = supply_cost,
                supply_unit=unit,
                amount_due=0,
                amount_paid=supply_cost
            )

        log = StockLog.objects.create(inventory=inventory, quantity=stock)

        return redirect("inventory")

    return render(request, "modals/stock_item.html")


@login_required(login_url="/users/login/")
def re_stock(request):
    user = request.user
    if request.method == "POST":

        amount = Decimal(request.POST.get("quantity"))
        product = int(request.POST.get("product"))
        payment_method = request.POST.get("payment_method")

        inventory = Inventory.objects.get(id=product)
        total_cost = inventory.unit_price * amount
        inventory.stock += amount

        if payment_method == "Credit":
            inventory.supplier.amount_owed += total_cost
            inventory.supplier.total_paid += 0
            inventory.supplier.total_supplies_cost += total_cost
            inventory.supplier.save()

        elif payment_method in ["Mpesa", "Cash"]:
            inventory.supplier.total_paid += total_cost
            inventory.supplier.amount_owed += 0
            inventory.supplier.total_supplies_cost += total_cost
            inventory.supplier.save()

        inventory.save()

        supply_log = SupplyLog.objects.create(
            supplier=inventory.supplier,
            item=inventory.name,
            quantity_supplied=amount,
            unit_price=inventory.unit_price,
            payment_method=payment_method,
            total_cost = total_cost,
            supply_unit=inventory.unit,
            amount_due=amount
        )

        log = StockLog.objects.create(
            inventory=inventory,
            quantity=amount,
            actioned_by=user,
            action="restock",
            destination="new_stock"
        )

        return redirect("inventory")

    return render(request, "modals/restock.html")


@login_required(login_url="/users/login/")
def take_out_stock(request):
    user = request.user
    if request.method == "POST":

        amount = Decimal(request.POST.get("quantity"))
        product = int(request.POST.get("product"))
        destination = request.POST.get("destination")

        inventory = Inventory.objects.get(id=product)
        inventory.stock -= amount
        inventory.save()

        log = StockLog.objects.create(
            inventory=inventory,
            quantity=amount,
            actioned_by=user,
            action="take_out",
            destination=destination
        )

        return redirect("inventory")
    return render(request, "modals/take_out_stock.html")


def stock_logs(request):
    stock_items = StockLog.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        stock_items = StockLog.objects.filter(
            Q(inventory__name__icontains=name))

    paginator = Paginator(stock_items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stock_items": stock_items,
        "page_obj": page_obj,
    }
    return render(request, "inventory/inventory_logs.html", context)


def pay_supplier(request):
    if request.method == "POST":
        supply_id = int(request.POST.get("supply_id"))
        amount = Decimal(request.POST.get("amount"))
        payment_method = request.POST.get("payment_method")

        supply = SupplyLog.objects.get(id=supply_id)

        supply.amount_due -= amount
        supply.amount_paid += amount
        supply.save()

        Expense.objects.create(
            title="Supply payment",
            purpose=f"Supply payment to {supply.supplier.name}",
            amount=amount,
            payment_method=payment_method
        )

        supply.supplier.total_paid += amount
        supply.supplier.amount_owed -= amount
        supply.supplier.save()

        return redirect("suppliers")

    return render(request, "suppliers/pay_supplier.html")