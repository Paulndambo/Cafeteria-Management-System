# Generated by Django 4.1.7 on 2023-10-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0009_alter_order_student"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[("Mpesa", "Mpesa"), ("Cash", "Cash"), ("Wallet", "Wallet")],
                max_length=255,
                null=True,
            ),
        ),
    ]
