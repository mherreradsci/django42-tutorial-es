# Generated by Django 4.2.3 on 2023-09-15 04:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0004_alter_customer_active_from"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="active",
        ),
    ]
