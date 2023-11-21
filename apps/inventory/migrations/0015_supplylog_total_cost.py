# Generated by Django 4.1.7 on 2023-11-21 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0014_supplier_amount_owed_supplylog"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplylog",
            name="total_cost",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
            preserve_default=False,
        ),
    ]
