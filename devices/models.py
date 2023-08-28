import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse

from common.models import ValidityInfo
from customers.models import Customer


class DeviceManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Device(ValidityInfo):
    code = models.CharField(unique=True, max_length=6, null=False, blank=False)
    customers = models.ManyToManyField(
        Customer, through="DeviCustAssignment", related_name="devices"
    )
    name = models.CharField(max_length=120, null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    ipv4 = models.GenericIPAddressField(
        protocol="IPv4", blank=True, null=True, default=None
    )
    ipv6 = models.GenericIPAddressField(
        protocol="IPv6", blank=True, null=True, default=None
    )

    objects = DeviceManager()

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

    def natural_key(self):
        return self.code


class DeviCustAssignment(ValidityInfo):
    CLOSING_REASON_TYPE = [
        ("SCH", "Scheduled"),
        ("EOC", "End of Contract"),
        ("DEC", "Decommissioned"),
        ("OOO", "Out Of Order"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    # Campos adicionales
    closing_reason_type = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(3)],
        choices=CLOSING_REASON_TYPE,
        null=True,
        blank=True,
    )
    closing_remarks = models.TextField(max_length=600, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = "Device Customer Assignment"
        verbose_name_plural = "Device Customer Assignments"

        db_table = "devi_cust_assignments"  # 'core"."devi_cust_assignments'
        db_table_comment = "Assignments of devices to customers"

        # Seún lo recomendado:
        # https://docs.djangoproject.com/en/4.2/ref/models/options/#unique-together
        # Si se implementa con UniqueConstraints
        # IMPORTANTE: Se debe utilizar los campos del modelo y no los de la BD,
        # si se utiliza los campos de la BD: 'customer_id', 'device_id' todo funciona
        # al hacer makemigrations y migrate, sin embargo, no funcionan bien las
        # validaciones del form.is_valid()

        constraints = [
            UniqueConstraint(
                fields=["customer", "device", "active_from"],
                name="devi_cust_assignment_uk01",
            ),
        ]

    def get_absolute_url(self):
        return reverse("devices:list")

    def __str__(self):
        return f"{self.customer} - {self.device}"
