# Generated by Django 4.2.3 on 2023-08-27 18:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0012_remove_devicustassignment_devi_cust_assignment_uk01"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="device",
            name="customers",
        ),
    ]
