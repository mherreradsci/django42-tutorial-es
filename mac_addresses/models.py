from django.db import models

from common.models import ValidityInfo
from devices.models import Device
from mac_address_types.models import MacAddressType
from mac_addresses.validators import validate_mac_address


class MacAddress(ValidityInfo):
    address = models.CharField(
        unique=True,
        max_length=17,
        null=False,
        blank=False,
        validators=[validate_mac_address],
    )
    maad_type = models.ForeignKey(
        MacAddressType,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    device = models.ForeignKey(
        Device, null=False, blank=False, on_delete=models.CASCADE
    )

    class Meta:
        managed = True
        verbose_name = "MAC Address"
        verbose_name_plural = "MAC Addresses"

        db_table = "mac_addresses"  # 'core"."mac_addresses'
        db_table_comment = "MAC adresses"
        indexes = [
            models.Index(fields=["address"], name="address_uk01"),
        ]

    def __str__(self):
        return f"[{self.address}]"

    # def get_absolute_url(self):
    #     return reverse("mac_addresses:list")
