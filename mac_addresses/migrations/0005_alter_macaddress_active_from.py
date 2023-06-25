# Generated by Django 4.2.2 on 2023-06-18 06:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mac_addresses", "0004_macaddress_active_from_macaddress_active_until"),
    ]

    operations = [
        migrations.AlterField(
            model_name="macaddress",
            name="active_from",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2023, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
    ]