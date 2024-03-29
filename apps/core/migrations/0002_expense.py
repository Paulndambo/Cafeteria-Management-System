# Generated by Django 4.1.7 on 2023-11-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
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
                ("title", models.CharField(max_length=255)),
                ("purpose", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
