from django.shortcuts import render, redirect
from decimal import Decimal
from apps.inventory.models import Inventory
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

        return redirect("inventory")


    return render(request, "modals/stock_item.html")