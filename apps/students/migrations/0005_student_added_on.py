# Generated by Django 4.1.7 on 2023-11-19 09:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0004_alter_walletrechargelog_amount_recharged"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="added_on",
            field=models.DateField(null=True),
        ),
    ]
