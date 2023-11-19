# Generated by Django 4.1.7 on 2023-11-19 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0005_student_added_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="credit_limit",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
    ]