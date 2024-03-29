# Generated by Django 4.1.7 on 2023-10-05 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("students", "0002_alter_studentwallet_student"),
        ("inventory", "0006_menu"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("total_cost", models.DecimalField(decimal_places=2, max_digits=20)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Cancelled", "Cancelled"),
                            ("Processed", "Processed"),
                            ("Pending", "Pending"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.student",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.FloatField(default=0)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.menu",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orderitems",
                        to="orders.order",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
