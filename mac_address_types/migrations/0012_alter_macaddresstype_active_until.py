# Generated by Django 4.2.2 on 2023-06-13 04:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mac_address_types", "0011_alter_macaddresstype_active_until"),
    ]

    operations = [
        migrations.AlterField(
            model_name="macaddresstype",
            name="active_until",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2500, 12, 31, 21, 0)
            ),
        ),
    ]
