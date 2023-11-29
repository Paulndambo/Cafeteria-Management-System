import csv
from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

date_today = datetime.now().date()
from datetime import date

# Create your views here.
from apps.reports.models import (DailySalesReport, DailySalesReportData,
                                 GeneralisedReportData, SalesReport)


def convert_to_date(datetime_field):
    if datetime_field:
        return datetime_field.date()
    return None


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
            today_sales_data = GeneralisedReportData.objects.all().delete()
            
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


def daily_sales_data(request):
    items_sold = SalesReport.objects.filter(created__date=date_today).filter(sold_or_spoiled="Sold")

    for sold_item in items_sold:
        item_exists = DailySalesReportData.objects.filter(item=sold_item.item, date_recorded__date=convert_to_date(sold_item.created)).first()

        if item_exists:
            item_exists.quantity += sold_item.quantity
            item_exists.amount += sold_item.amount
            item_exists.save()
        else:
            DailySalesReportData.objects.create(
                date_recorded=sold_item.created,
                item=sold_item.item,
                quantity=sold_item.quantity,
                amount=sold_item.amount,
                unit_price=sold_item.unit_price,
                sold_or_spoiled="Sold"
            )
    
    daily_sales_data = DailySalesReportData.objects.all()
    
    
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        action_type = request.POST.get("action_type")

        starting_date = request.POST.get("starting_date")
        ending_date = request.POST.get("ending_date")

       
        print(f"Action Type: {action_type}")

        if start_date and end_date:
    
            daily_sales_data = DailySalesReportData.objects.filter(
                date_recorded__date__gte=start_date
            ).filter(date_recorded__date__lte=end_date)


        if action_type == "export" and starting_date and ending_date:

            print(f"Starting Date: {starting_date}, Ending Date: {ending_date}")

            filtered_report = DailySalesReportData.objects.filter(
                date_recorded__date__gte=starting_date
            ).filter(date_recorded__date__lte=ending_date)

            response = HttpResponse(content_type='text/csv')
            file_name =  f'attachment; filename="Daily Item Sales General Report.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold", "Unit Price", "Quantity", "Sales Total"]) 
            daily_item_sales_values = filtered_report.values_list('id', 'date_recorded__date', 'item', 'unit_price', 'quantity', 'amount')       

            for daily_item_sale in daily_item_sales_values:
                writer.writerow(daily_item_sale)
            
            return response

        print(f"Start Date: {start_date}, End Date: {end_date}")

    
    #if request.method == "POST":
        

    
    paginator = Paginator(daily_sales_data, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "daily_sales": daily_sales_data,
        "page_obj": page_obj
    }
    return render(request, "reports/daily_sales.html", context)