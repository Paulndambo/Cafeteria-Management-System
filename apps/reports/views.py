import csv
from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

date_today = datetime.now().date()
# Create your views here.
from apps.reports.models import (DailySalesReport, GeneralisedReportData,
                                 SalesReport)


def today_sales_report(request): 
    items_sold_today = SalesReport.objects.filter(created__date=date_today, sold_or_spoiled="Sold")
    sales_total = sum(list(SalesReport.objects.filter(created__date=date_today, sold_or_spoiled="Sold").values_list("amount", flat=True)))
   
    paginator = Paginator(items_sold_today, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    
    report_data = list(
        DailySalesReport.objects.filter(created__date=date_today).values('payment_method')
        .annotate(total_sales_amount=Sum('amount'))
        .order_by('payment_method')
    )


    if request.method == "POST":
        action_type = request.POST.get("action_type")
        print(f"Action Type: {action_type}")
        
        if action_type == "item_sales":   
            for x in items_sold_today:
                gen = GeneralisedReportData.objects.filter(item=x.item, created__date=date_today).first()

                if gen:
                    gen.quantity += x.quantity
                    gen.amount += x.amount
                    gen.save()
                else:
                    GeneralisedReportData.objects.create(
                        item=x.item,
                        quantity=x.quantity,
                        amount=x.amount,
                        unit_price=x.unit_price,
                        sold_or_spoiled="Sold"
                    )

            
            today_sales_data = GeneralisedReportData.objects.all()

            response = HttpResponse(content_type='text/csv')
            file_name =  f'attachment; filename="Daily Item Sales Report - {date_today}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold", "Unit Price", "Quantity", "Sales Total"]) 
            daily_item_sales_values = today_sales_data.values_list('id', 'created__date', 'item', 'unit_price', 'quantity', 'amount')       

            for daily_item_sale in daily_item_sales_values:
                writer.writerow(daily_item_sale)
            writer.writerow(["", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", sales_total])
            return response
            

        elif action_type == "overall_sales":
            csv_data = [['Report Date', 'Payment Method', 'Total Sales Amount']]
            for entry in report_data:
                csv_data.append([date_today, entry['payment_method'], entry['total_sales_amount']])

            # Create CSV response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Daily Overall Sales Report.csv"'

            # Write CSV data to the response
            writer = csv.writer(response)
            writer.writerows(csv_data)
            return response
        

    context = {
        "page_obj": page_obj
    }
    return render(request, "reports/sales_today.html", context)