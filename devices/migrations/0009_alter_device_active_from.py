# Generated by Django 4.2.2 on 2023-06-25 19:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0008_alter_device_active_from"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="active_from",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]