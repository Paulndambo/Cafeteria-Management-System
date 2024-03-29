# Generated by Django 4.1.7 on 2023-10-04 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("inventory", "0003_stocklog"),
    ]

    operations = [
        migrations.AddField(
            model_name="stocklog",
            name="action",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="stocklog",
            name="actioned_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="stocklog",
            name="destination",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
