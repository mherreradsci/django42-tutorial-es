# Generated by Django 4.2.2 on 2023-06-25 19:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0003_customer_active_customer_active_from_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="active_from",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]
