# Generated by Django 4.1.7 on 2023-11-21 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0016_alter_supplylog_supplier"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplylog",
            name="supply_unit",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
