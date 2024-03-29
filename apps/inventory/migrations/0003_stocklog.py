# Generated by Django 4.1.7 on 2023-09-06 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0002_alter_inventory_unit"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "inventory",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.inventory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
