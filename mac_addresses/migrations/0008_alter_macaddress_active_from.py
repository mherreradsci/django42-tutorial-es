# Generated by Django 4.2.3 on 2023-09-30 05:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mac_addresses", "0007_remove_macaddress_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="macaddress",
            name="active_from",
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
