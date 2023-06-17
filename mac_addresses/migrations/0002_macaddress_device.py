# Generated by Django 4.2.2 on 2023-06-14 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0006_alter_device_created_by_alter_device_updated_by"),
        ("mac_addresses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="macaddress",
            name="device",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="devices.device",
            ),
            preserve_default=False,
        ),
    ]