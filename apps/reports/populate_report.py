from datetime import date, datetime

from apps.reports.models import DailySalesReportData, SalesReport

date_today = datetime.now().date()


def convert_to_date(datetime_field):
    if datetime_field:
        return datetime_field.date()
    return None



def update_report_from_prev_days():
    items_sold = SalesReport.objects.filter(sold_or_spoiled="Sold").exclude(created__date=date_today)

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