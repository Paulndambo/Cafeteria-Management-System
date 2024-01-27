from apps.reports.models import DailySalesReport


class DailyReportMixin(object):
    def __init__(self, order, recharge_method, order_value, amount):
        self.order = order
        self.recharge_method = recharge_method
        self.order_value = order_value
        self.amount = amount
           

    def run(self):
        self.__create_report_instance()

    def __create_report_instance(self):
        if self.recharge_method == "Mpesa":
            DailySalesReport.objects.create(
                order=self.order,
                payment_method="Wallet",
                amount=self.order_value-self.amount,
            )
            DailySalesReport.objects.create(
                order=self.order,
                payment_method="Mpesa",
                amount=self.amount,
            )
        elif self.recharge_method == "Cash":
            DailySalesReport.objects.create(
                order=self.order,
                payment_method="Wallet",
                amount=self.order_value-self.amount,
            )
            DailySalesReport.objects.create(
                order=self.order,
                payment_method="Cash",
                amount=self.amount,
            )