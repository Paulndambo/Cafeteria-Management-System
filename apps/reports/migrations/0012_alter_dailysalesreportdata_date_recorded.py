# Generated by Django 4.1.7 on 2023-11-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0011_dailysalesreportdata_date_recorded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailysalesreportdata",
            name="date_recorded",
            field=models.DateTimeField(null=True),
        ),
    ]
