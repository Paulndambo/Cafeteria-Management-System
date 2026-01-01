import csv
from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpRequest

import calendar
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Q, Avg
from apps.orders.models import Order
from apps.core.models import Expense
from apps.reports.models import DailySalesReport, SalesReport

date_today = datetime.now().date()
from datetime import date

# Create your views here.
from apps.reports.models import (DailySalesReport, DailySalesReportData,
                                 GeneralisedReportData, SalesReport)


def convert_to_date(datetime_field):
    if datetime_field:
        return datetime_field.date()
    return None


def today_sales_report(request: HttpRequest): 
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


def daily_sales_data(request: HttpRequest):
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


        if action_type == "export_item_sales" and starting_date and ending_date:

            print(f"Starting Date: {starting_date}, Ending Date: {ending_date}")

            # Get SalesReport data and aggregate by item
            sales_data = SalesReport.objects.filter(
                created__date__gte=starting_date,
                created__date__lte=ending_date,
                sold_or_spoiled="Sold"
            ).values('item', 'unit_price').annotate(
                total_quantity=Sum('quantity'),
                total_amount=Sum('amount')
            ).order_by('item')

            response = HttpResponse(content_type='text/csv')
            file_name = f'attachment; filename="Daily Item Sales Report - {starting_date} to {ending_date}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold", "Unit Price", "Quantity", "Sales Total"]) 
            
            # Write aggregated data
            for idx, sale in enumerate(sales_data, start=1):
                writer.writerow([
                    idx,
                    f"{starting_date} to {ending_date}",
                    sale['item'],
                    sale['unit_price'],
                    sale['total_quantity'],
                    sale['total_amount']
                ])
            
            # Add total row
            total_sales = sum(sale['total_amount'] for sale in sales_data)
            writer.writerow(["", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", total_sales])
            
            return response

        elif action_type == "export_payment_method" and starting_date and ending_date:

            print(f"Payment Method Report - Starting Date: {starting_date}, Ending Date: {ending_date}")

            # Get DailySalesReport data grouped by payment method
            payment_data = DailySalesReport.objects.filter(
                created__date__gte=starting_date,
                created__date__lte=ending_date
            ).values('payment_method').annotate(
                total_sales_amount=Sum('amount')
            ).order_by('payment_method')

            response = HttpResponse(content_type='text/csv')
            file_name = f'attachment; filename="Payment Method Sales Report - {starting_date} to {ending_date}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["Report Date", "Payment Method", "Total Sales Amount"]) 
            
            # Write payment method data
            for payment in payment_data:
                writer.writerow([
                    f"{starting_date} to {ending_date}",
                    payment['payment_method'],
                    payment['total_sales_amount']
                ])
            
            # Add total row
            total_amount = sum(payment['total_sales_amount'] for payment in payment_data)
            writer.writerow(["", "", ""])
            writer.writerow(["Total", "", total_amount])
            
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



def summary_stats(request: HttpRequest):
    # Get filter parameters
    filter_date = request.GET.get('date')
    filter_month = request.GET.get('month')
    filter_year = request.GET.get('year')
    
    # Initialize querysets
    orders_qs = Order.objects.all()

    expenses_qs = Expense.objects.all()
    sales_report_qs = DailySalesReport.objects.all()
    sales_data_qs = SalesReport.objects.filter(sold_or_spoiled="Sold")
    
    # Apply filters
    if filter_date:
        orders_qs = orders_qs.filter(created__date=filter_date)
        expenses_qs = expenses_qs.filter(expense_date=filter_date)
        sales_report_qs = sales_report_qs.filter(created__date=filter_date)
        sales_data_qs = sales_data_qs.filter(created__date=filter_date)
    elif filter_month and filter_year:
        orders_qs = orders_qs.filter(month=filter_month, year=int(filter_year))
        expenses_qs = expenses_qs.filter(month=filter_month, year=filter_year)
        # For sales reports, filter by created date
        month_num = list(calendar.month_name).index(filter_month)
        start_date = datetime(int(filter_year), month_num, 1).date()
        # Get last day of month
        last_day = calendar.monthrange(int(filter_year), month_num)[1]
        end_date = datetime(int(filter_year), month_num, last_day).date()
        sales_report_qs = sales_report_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
        sales_data_qs = sales_data_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
    elif filter_year:
        orders_qs = orders_qs.filter(year=int(filter_year))
        expenses_qs = expenses_qs.filter(year=filter_year)
        start_date = datetime(int(filter_year), 1, 1).date()
        end_date = datetime(int(filter_year), 12, 31).date()
        sales_report_qs = sales_report_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
        sales_data_qs = sales_data_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
    
    # Calculate statistics
    total_orders = orders_qs.count()
    orders_processed = orders_qs.filter(status="Processed").count()
    orders_pending = orders_qs.filter(status="Pending").count()
    orders_cancelled = orders_qs.filter(status="Cancelled").count()
    
    # Sales statistics
    total_sales = sales_report_qs.aggregate(total=Sum('amount'))['total'] or 0
    wallet_sales = sales_report_qs.filter(payment_method="Wallet").aggregate(total=Sum('amount'))['total'] or 0
    cash_sales = sales_report_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_sales = sales_report_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Expenses
    total_expenses = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    cash_expenses = expenses_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_expenses = expenses_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Profit/Loss
    net_profit = total_sales - total_expenses
    
    # Items statistics
    total_items_sold = sales_data_qs.aggregate(total=Sum('quantity'))['total'] or 0
    spoiled_qs = SalesReport.objects.filter(sold_or_spoiled="Spoiled")
    if filter_date:
        spoiled_qs = spoiled_qs.filter(created__date=filter_date)
    elif filter_month and filter_year:
        month_num = list(calendar.month_name).index(filter_month)
        start_date = datetime(int(filter_year), month_num, 1).date()
        last_day = calendar.monthrange(int(filter_year), month_num)[1]
        end_date = datetime(int(filter_year), month_num, last_day).date()
        spoiled_qs = spoiled_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
    elif filter_year:
        start_date = datetime(int(filter_year), 1, 1).date()
        end_date = datetime(int(filter_year), 12, 31).date()
        spoiled_qs = spoiled_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
    total_items_spoiled = spoiled_qs.count()
    
    # Average order value
    avg_order_value = orders_qs.aggregate(avg=Avg('total_cost'))['avg'] or 0
    
    # Get unique items sold
    unique_items_sold = sales_data_qs.values('item').distinct().count()
    
    # Get month names for dropdown
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Get available years from orders
    available_years = list(Order.objects.values_list('year', flat=True).distinct().exclude(year__isnull=True).order_by('-year'))
    # If no years found, add current year
    if not available_years:
        from datetime import date
        available_years = [date.today().year]
    
    context = {
        'total_orders': total_orders,
        'orders_processed': orders_processed,
        'orders_pending': orders_pending,
        'orders_cancelled': orders_cancelled,
        'total_sales': total_sales,
        'wallet_sales': wallet_sales,
        'cash_sales': cash_sales,
        'mpesa_sales': mpesa_sales,
        'total_expenses': total_expenses,
        'cash_expenses': cash_expenses,
        'mpesa_expenses': mpesa_expenses,
        'net_profit': net_profit,
        'total_items_sold': total_items_sold,
        'total_items_spoiled': total_items_spoiled,
        'avg_order_value': avg_order_value,
        'unique_items_sold': unique_items_sold,
        'filter_date': filter_date,
        'filter_month': filter_month,
        'filter_year': filter_year,
        'months': months,
        'available_years': available_years,
    }
    return render(request, "reports/summary_stats.html", context)



def weekly_stats(request: HttpRequest):
    # Get filter parameters from GET or POST
    start_date = request.GET.get('start_date') or request.POST.get('start_date')
    end_date = request.GET.get('end_date') or request.POST.get('end_date')
    action_type = request.POST.get('action_type')
    
    # Initialize querysets
    orders_qs = Order.objects.all()
    expenses_qs = Expense.objects.all()
    sales_report_qs = DailySalesReport.objects.all()
    sales_data_qs = SalesReport.objects.filter(sold_or_spoiled="Sold")
    spoiled_qs = SalesReport.objects.filter(sold_or_spoiled="Spoiled")
    
    # Apply date range filters
    if start_date and end_date:
        orders_qs = orders_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
        expenses_qs = expenses_qs.filter(expense_date__gte=start_date, expense_date__lte=end_date)
        sales_report_qs = sales_report_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
        sales_data_qs = sales_data_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
        spoiled_qs = spoiled_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
    
    # Handle CSV export requests
    if request.method == "POST" and action_type:
        if action_type == "export_item_sales":
            # Get SalesReport data and aggregate by item only (group by item name)
            sales_data = sales_data_qs.values('item').annotate(
                avg_unit_price=Avg('unit_price'),
                total_quantity=Sum('quantity'),
                total_amount=Sum('amount')
            ).order_by('item')

            response = HttpResponse(content_type='text/csv')
            date_range = f"{start_date} to {end_date}" if start_date and end_date else "All Time"
            file_name = f'attachment; filename="Weekly Item Sales Report - {date_range}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold", "Unit Price", "Quantity", "Sales Total"]) 
            
            # Write aggregated data
            for idx, sale in enumerate(sales_data, start=1):
                writer.writerow([
                    idx,
                    date_range,
                    sale['item'],
                    f"{sale['avg_unit_price']:.2f}",
                    sale['total_quantity'],
                    sale['total_amount']
                ])
            
            # Add total row
            total_sales = sum(sale['total_amount'] for sale in sales_data)
            writer.writerow(["", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", total_sales])
            
            return response

        elif action_type == "export_payment_method":
            # Get DailySalesReport data grouped by payment method
            payment_data = sales_report_qs.values('payment_method').annotate(
                total_sales_amount=Sum('amount')
            ).order_by('payment_method')

            response = HttpResponse(content_type='text/csv')
            date_range = f"{start_date} to {end_date}" if start_date and end_date else "All Time"
            file_name = f'attachment; filename="Weekly Payment Method Sales Report - {date_range}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["Report Date", "Payment Method", "Total Sales Amount"]) 
            
            # Write payment method data
            for payment in payment_data:
                writer.writerow([
                    date_range,
                    payment['payment_method'],
                    payment['total_sales_amount']
                ])
            
            # Add total row
            total_amount = sum(payment['total_sales_amount'] for payment in payment_data)
            writer.writerow(["", "", ""])
            writer.writerow(["Total", "", total_amount])
            
            return response
    
    # Calculate statistics
    total_orders = orders_qs.count()
    orders_processed = orders_qs.filter(status="Processed").count()
    orders_pending = orders_qs.filter(status="Pending").count()
    orders_cancelled = orders_qs.filter(status="Cancelled").count()
    
    # Sales statistics
    total_sales = sales_report_qs.aggregate(total=Sum('amount'))['total'] or 0
    wallet_sales = sales_report_qs.filter(payment_method="Wallet").aggregate(total=Sum('amount'))['total'] or 0
    cash_sales = sales_report_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_sales = sales_report_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Expenses
    total_expenses = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    cash_expenses = expenses_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_expenses = expenses_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Profit/Loss
    net_profit = total_sales - total_expenses
    
    # Items statistics
    total_items_sold = sales_data_qs.aggregate(total=Sum('quantity'))['total'] or 0
    total_items_spoiled = spoiled_qs.count()
    
    # Average order value
    avg_order_value = orders_qs.aggregate(avg=Avg('total_cost'))['avg'] or 0
    
    # Get unique items sold
    unique_items_sold = sales_data_qs.values('item').distinct().count()
    
    context = {
        'total_orders': total_orders,
        'orders_processed': orders_processed,
        'orders_pending': orders_pending,
        'orders_cancelled': orders_cancelled,
        'total_sales': total_sales,
        'wallet_sales': wallet_sales,
        'cash_sales': cash_sales,
        'mpesa_sales': mpesa_sales,
        'total_expenses': total_expenses,
        'cash_expenses': cash_expenses,
        'mpesa_expenses': mpesa_expenses,
        'net_profit': net_profit,
        'total_items_sold': total_items_sold,
        'total_items_spoiled': total_items_spoiled,
        'avg_order_value': avg_order_value,
        'unique_items_sold': unique_items_sold,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, "reports/weekly_stats.html", context)


def daily_stats(request: HttpRequest):
    # Get filter parameter from GET or POST
    filter_date = request.GET.get('date') or request.POST.get('filter_date')
    action_type = request.POST.get('action_type')
    
    # Initialize querysets
    orders_qs = Order.objects.all()
    expenses_qs = Expense.objects.all()
    sales_report_qs = DailySalesReport.objects.all()
    sales_data_qs = SalesReport.objects.filter(sold_or_spoiled="Sold")
    spoiled_qs = SalesReport.objects.filter(sold_or_spoiled="Spoiled")
    
    # Apply date filter
    if filter_date:
        orders_qs = orders_qs.filter(created__date=filter_date)
        expenses_qs = expenses_qs.filter(expense_date=filter_date)
        sales_report_qs = sales_report_qs.filter(created__date=filter_date)
        sales_data_qs = sales_data_qs.filter(created__date=filter_date)
        spoiled_qs = spoiled_qs.filter(created__date=filter_date)
    
    # Handle CSV export requests
    if request.method == "POST" and action_type:
        if action_type == "export_item_sales":
            # Get SalesReport data and aggregate by item only (group by item name)
            sales_data = sales_data_qs.values('item').annotate(
                avg_unit_price=Avg('unit_price'),
                total_quantity=Sum('quantity'),
                total_amount=Sum('amount')
            ).order_by('item')

            response = HttpResponse(content_type='text/csv')
            date_str = filter_date if filter_date else "All Dates"
            file_name = f'attachment; filename="Daily Item Sales Report - {date_str}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold", "Unit Price", "Quantity", "Sales Total"]) 
            
            # Write aggregated data
            for idx, sale in enumerate(sales_data, start=1):
                writer.writerow([
                    idx,
                    date_str,
                    sale['item'],
                    f"{sale['avg_unit_price']:.2f}",
                    sale['total_quantity'],
                    sale['total_amount']
                ])
            
            # Add total row
            total_sales = sum(sale['total_amount'] for sale in sales_data)
            writer.writerow(["", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", total_sales])
            
            return response

        elif action_type == "export_payment_method":
            # Get DailySalesReport data grouped by payment method
            payment_data = sales_report_qs.values('payment_method').annotate(
                total_sales_amount=Sum('amount')
            ).order_by('payment_method')

            response = HttpResponse(content_type='text/csv')
            date_str = filter_date if filter_date else "All Dates"
            file_name = f'attachment; filename="Payment Method Sales Report - {date_str}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["Report Date", "Payment Method", "Total Sales Amount"]) 
            
            # Write payment method data
            for payment in payment_data:
                writer.writerow([
                    date_str,
                    payment['payment_method'],
                    payment['total_sales_amount']
                ])
            
            # Add total row
            total_amount = sum(payment['total_sales_amount'] for payment in payment_data)
            writer.writerow(["", "", ""])
            writer.writerow(["Total", "", total_amount])
            
            return response
    
    # Calculate statistics
    total_orders = orders_qs.count()
    orders_processed = orders_qs.filter(status="Processed").count()
    orders_pending = orders_qs.filter(status="Pending").count()
    orders_cancelled = orders_qs.filter(status="Cancelled").count()
    
    # Sales statistics
    total_sales = sales_report_qs.aggregate(total=Sum('amount'))['total'] or 0
    wallet_sales = sales_report_qs.filter(payment_method="Wallet").aggregate(total=Sum('amount'))['total'] or 0
    cash_sales = sales_report_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_sales = sales_report_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Expenses
    total_expenses = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    cash_expenses = expenses_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_expenses = expenses_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Profit/Loss
    net_profit = total_sales - total_expenses
    
    # Items statistics
    total_items_sold = sales_data_qs.aggregate(total=Sum('quantity'))['total'] or 0
    total_items_spoiled = spoiled_qs.count()
    
    # Average order value
    avg_order_value = orders_qs.aggregate(avg=Avg('total_cost'))['avg'] or 0
    
    # Get unique items sold
    unique_items_sold = sales_data_qs.values('item').distinct().count()
    
    context = {
        'total_orders': total_orders,
        'orders_processed': orders_processed,
        'orders_pending': orders_pending,
        'orders_cancelled': orders_cancelled,
        'total_sales': total_sales,
        'wallet_sales': wallet_sales,
        'cash_sales': cash_sales,
        'mpesa_sales': mpesa_sales,
        'total_expenses': total_expenses,
        'cash_expenses': cash_expenses,
        'mpesa_expenses': mpesa_expenses,
        'net_profit': net_profit,
        'total_items_sold': total_items_sold,
        'total_items_spoiled': total_items_spoiled,
        'avg_order_value': avg_order_value,
        'unique_items_sold': unique_items_sold,
        'filter_date': filter_date,
    }
    return render(request, "reports/daily_stats.html", context)


def monthly_stats(request: HttpRequest):
    # Get filter parameters from GET or POST
    filter_month = request.GET.get('month') or request.POST.get('filter_month')
    filter_year = request.GET.get('year') or request.POST.get('filter_year')
    action_type = request.POST.get('action_type')
    
    # Initialize querysets
    orders_qs = Order.objects.all()
    expenses_qs = Expense.objects.all()
    sales_report_qs = DailySalesReport.objects.all()
    sales_data_qs = SalesReport.objects.filter(sold_or_spoiled="Sold")
    spoiled_qs = SalesReport.objects.filter(sold_or_spoiled="Spoiled")
    
    # Apply month and year filters
    start_date = None
    end_date = None
    if filter_month and filter_year:
        orders_qs = orders_qs.filter(month=filter_month, year=int(filter_year))
        expenses_qs = expenses_qs.filter(month=filter_month, year=filter_year)
        # For sales reports, filter by created date
        month_num = list(calendar.month_name).index(filter_month)
        start_date = datetime(int(filter_year), month_num, 1).date()
        # Get last day of month
        last_day = calendar.monthrange(int(filter_year), month_num)[1]
        end_date = datetime(int(filter_year), month_num, last_day).date()
        sales_report_qs = sales_report_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
        sales_data_qs = sales_data_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
        spoiled_qs = spoiled_qs.filter(created__date__gte=start_date, created__date__lte=end_date)
    
    # Handle CSV export requests
    if request.method == "POST" and action_type:
        if action_type == "export_item_sales":
            # Get SalesReport data and aggregate by item only (group by item name)
            sales_data = sales_data_qs.values('item').annotate(
                avg_unit_price=Avg('unit_price'),
                total_quantity=Sum('quantity'),
                total_amount=Sum('amount')
            ).order_by('item')

            response = HttpResponse(content_type='text/csv')
            period_str = f"{filter_month} {filter_year}" if filter_month and filter_year else "All Time"
            file_name = f'attachment; filename="Monthly Item Sales Report - {period_str}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold", "Unit Price", "Quantity", "Sales Total"]) 
            
            # Write aggregated data
            for idx, sale in enumerate(sales_data, start=1):
                writer.writerow([
                    idx,
                    period_str,
                    sale['item'],
                    f"{sale['avg_unit_price']:.2f}",
                    sale['total_quantity'],
                    sale['total_amount']
                ])
            
            # Add total row
            total_sales = sum(sale['total_amount'] for sale in sales_data)
            writer.writerow(["", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", total_sales])
            
            return response

        elif action_type == "export_payment_method":
            # Get DailySalesReport data grouped by payment method
            payment_data = sales_report_qs.values('payment_method').annotate(
                total_sales_amount=Sum('amount')
            ).order_by('payment_method')

            response = HttpResponse(content_type='text/csv')
            period_str = f"{filter_month} {filter_year}" if filter_month and filter_year else "All Time"
            file_name = f'attachment; filename="Monthly Payment Method Sales Report - {period_str}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["Report Date", "Payment Method", "Total Sales Amount"]) 
            
            # Write payment method data
            for payment in payment_data:
                writer.writerow([
                    period_str,
                    payment['payment_method'],
                    payment['total_sales_amount']
                ])
            
            # Add total row
            total_amount = sum(payment['total_sales_amount'] for payment in payment_data)
            writer.writerow(["", "", ""])
            writer.writerow(["Total", "", total_amount])
            
            return response
    
    # Calculate statistics
    total_orders = orders_qs.count()
    orders_processed = orders_qs.filter(status="Processed").count()
    orders_pending = orders_qs.filter(status="Pending").count()
    orders_cancelled = orders_qs.filter(status="Cancelled").count()
    
    # Sales statistics
    total_sales = sales_report_qs.aggregate(total=Sum('amount'))['total'] or 0
    wallet_sales = sales_report_qs.filter(payment_method="Wallet").aggregate(total=Sum('amount'))['total'] or 0
    cash_sales = sales_report_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_sales = sales_report_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Expenses
    total_expenses = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    cash_expenses = expenses_qs.filter(payment_method="Cash").aggregate(total=Sum('amount'))['total'] or 0
    mpesa_expenses = expenses_qs.filter(payment_method="Mpesa").aggregate(total=Sum('amount'))['total'] or 0
    
    # Profit/Loss
    net_profit = total_sales - total_expenses
    
    # Items statistics
    total_items_sold = sales_data_qs.aggregate(total=Sum('quantity'))['total'] or 0
    total_items_spoiled = spoiled_qs.count()
    
    # Average order value
    avg_order_value = orders_qs.aggregate(avg=Avg('total_cost'))['avg'] or 0
    
    # Get unique items sold
    unique_items_sold = sales_data_qs.values('item').distinct().count()
    
    # Get month names for dropdown
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Get available years from orders
    available_years = list(Order.objects.values_list('year', flat=True).distinct().exclude(year__isnull=True).order_by('-year'))
    # If no years found, add current year
    if not available_years:
        from datetime import date
        available_years = [date.today().year]
    
    context = {
        'total_orders': total_orders,
        'orders_processed': orders_processed,
        'orders_pending': orders_pending,
        'orders_cancelled': orders_cancelled,
        'total_sales': total_sales,
        'wallet_sales': wallet_sales,
        'cash_sales': cash_sales,
        'mpesa_sales': mpesa_sales,
        'total_expenses': total_expenses,
        'cash_expenses': cash_expenses,
        'mpesa_expenses': mpesa_expenses,
        'net_profit': net_profit,
        'total_items_sold': total_items_sold,
        'total_items_spoiled': total_items_spoiled,
        'avg_order_value': avg_order_value,
        'unique_items_sold': unique_items_sold,
        'filter_month': filter_month,
        'filter_year': filter_year,
        'months': months,
        'available_years': available_years,
    }
    return render(request, "reports/monthly_stats.html", context)