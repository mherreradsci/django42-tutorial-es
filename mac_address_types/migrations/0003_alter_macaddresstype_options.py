# Generated by Django 4.2.1 on 2023-06-11 05:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mac_address_types", "0002_rename_macaddesstype_macaddresstype"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="macaddresstype",
            options={
                "managed": True,
                "verbose_name": "MAC_address_type",
                "verbose_name_plural": "mac_address_types",
            },
        ),
    ]
