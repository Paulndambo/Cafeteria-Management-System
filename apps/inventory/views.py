from django.shortcuts import render, redirect
from decimal import Decimal
from apps.inventory.models import Inventory, StockLog
# Create your views here.
def inventory(request):
    stock_items = Inventory.objects.all()

    context = {
        "stock_items": stock_items
    }
    return render(request, "inventory/inventory.html", context)


def new_stock_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        unit = request.POST.get("unit")
        unit_price = Decimal(request.POST.get("unit_price"))
        selling_price = Decimal(request.POST.get("selling_price"))
        stock = Decimal(request.POST.get("stock"))

        inventory = Inventory.objects.create(
            name=name,
            unit_price=unit_price,
            selling_price=selling_price,
            unit=unit,
            stock=stock
        )

        log = StockLog.objects.create(inventory=inventory, quantity=stock)

        return redirect("inventory")


    return render(request, "modals/stock_item.html")


def re_stock(request):
    if request.method == "POST":

        amount = Decimal(request.POST.get("quantity"))
        product = int(request.POST.get("product"))

        inventory = Inventory.objects.get(id=product)
        inventory.stock += amount
        inventory.save()

        log = StockLog.objects.create(inventory=inventory, quantity=amount)
        
        return redirect("inventory")

    return render(request, "modals/restock.html")


def take_out_stock(request):
    if request.method == "POST":

        amount = Decimal(request.POST.get("quantity"))
        product = int(request.POST.get("product"))

        inventory = Inventory.objects.get(id=product)
        inventory.stock -= amount
        inventory.save()

        log = StockLog.objects.create(inventory=inventory, quantity=amount)
        
        return redirect("inventory")
    return render(request, "modals/take_out_stock.html")