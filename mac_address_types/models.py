from django.db import models
from common.models import TypeInfo, AuditInfo

# from django.conf import settings
from django.urls import reverse


class MacAddressType(TypeInfo):
    code = models.CharField(unique=True, max_length=12, null=True, blank=False)
    name = models.CharField(max_length=120, null=True, blank=True)
    desc = models.TextField(max_length=600, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = "MAC Address Type"
        verbose_name_plural = "MAC Address Types"
        db_table = "mac_address_types"  # 'core"."mac_address_types'
        db_table_comment = (
            "Media Access Control (MAC) Address Type."
            + "Types: Unicast MAC address; Multicast MAC address; Broadcast MAC address"
        )

    def __str__(self):
        return f"[{self.code}] {self.desc}"

    def get_absolute_url(self):
        return reverse("mac_address_types:list")
