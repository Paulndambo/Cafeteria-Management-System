# Generated by Django 4.1.7 on 2023-11-24 06:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0003_remove_salesreport_total_cost_salesreport_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salesreport",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("Mpesa", "Mpesa"),
                    ("Cash", "Cash"),
                    ("Wallet", "Wallet"),
                    ("No Payment", "No Payment"),
                ],
                max_length=255,
            ),
        ),
    ]
