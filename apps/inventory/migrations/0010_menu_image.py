# Generated by Django 4.1.7 on 2023-10-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0009_menu_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="image",
            field=models.ImageField(null=True, upload_to="menu_images"),
        ),
    ]
