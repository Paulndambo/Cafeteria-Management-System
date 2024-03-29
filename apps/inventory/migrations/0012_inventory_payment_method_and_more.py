# Generated by Django 4.1.7 on 2023-11-21 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0011_menu_starting_stock"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventory",
            name="payment_method",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="selling_price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, null=True
            ),
        ),
    ]
