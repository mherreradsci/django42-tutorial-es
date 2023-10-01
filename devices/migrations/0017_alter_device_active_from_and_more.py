# Generated by Django 4.2.3 on 2023-09-30 05:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0016_remove_device_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="active_from",
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="devicustassignment",
            name="active_from",
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
