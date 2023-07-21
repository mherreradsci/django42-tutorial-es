from django.db import models
from django.urls import reverse
from common.models import ValidityInfo
import uuid

from django.conf import settings


# User = settings.AUTH_USER_MODEL


class Device(ValidityInfo):
    code = models.CharField(unique=True, max_length=6, null=True, blank=False)
    name = models.CharField(max_length=120, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    ipv4 = models.GenericIPAddressField(
        protocol="IPv4", blank=True, null=True, default=None
    )
    ipv6 = models.GenericIPAddressField(
        protocol="IPv6", blank=True, null=True, default=None
    )

    class Meta:
        managed = True
        verbose_name = "device"
        verbose_name_plural = "devices"

        db_table = "devices"  # 'core"."devices'
        db_table_comment = (
            "Devices to be managed such as Webcam, Sensors, System-On-Module (SOM)"
        )
        indexes = [
            models.Index(fields=["name"], name="devices_ix01"),
        ]

    def __str__(self):
        return f"[{self.code}] {self.name}"

    def get_absolute_url(self):
        return reverse("devices:list")

    def get_macaddress(self):
        return self.macaddress_set.all()
