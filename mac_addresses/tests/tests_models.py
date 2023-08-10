from unittest import mock

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from devices.models import Device
from mac_address_types.models import MacAddressType
from mac_addresses.models import MacAddress

"""
Automated Test for MacAddresss Model
"""


class MacAddressTestCase(TestCase):
    # fixtures = ["init_mac_address.json"]
    def setUp(self):
        """
        Setup
        """
        User.objects.create(username="init")

    @classmethod
    def setUpTestData(cls):
        cls.number_of_mac_address = 50
        cls.mocked_created_at = timezone.now()

        cls.user = User.objects.create(username="testuser", password="password")
        cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
        cls.mac_address_type.save()
        cls.device = Device(code="ND", name="New Device Name")
        cls.device.save()

        # created_at and updated_at must have the same datetime when the recors
        # are created
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=cls.mocked_created_at)
        ):
            for id in range(0, cls.number_of_mac_address):
                MacAddress.objects.create(
                    address=str(id).zfill(2)
                    + "-"
                    + str(id).zfill(2)
                    + "-"
                    + str(id).zfill(2)
                    + "-"
                    + str(id).zfill(2)
                    + "-"
                    + str(id).zfill(2)
                    + "-"
                    + str(id).zfill(2),
                    maad_type=cls.mac_address_type,
                    device=cls.device,
                )

    def test_string_representation(self):
        object = MacAddress.objects.first()
        self.assertEqual(str(object), f"[{object.address}]")

    def test_verbose_name_plural(self):
        self.assertEqual(str(MacAddress._meta.verbose_name_plural), "MAC Addresses")

    def test_query_set_exists(self):
        qs = MacAddress.objects.all()
        self.assertTrue(qs.exists())

    def test_query_counts(self):
        qs = MacAddress.objects.all()
        self.assertEqual(qs.count(), self.number_of_mac_address)

    def test_validate_created_at(self):
        object = MacAddress.objects.filter(address__exact="00-00-00-00-00-00")[0]

        self.assertEqual(
            self.mocked_created_at, object.created_at + timezone.timedelta(days=0)
        )

    def test_updated_at(self):
        object = MacAddress.objects.order_by("id").last()
        self.assertEqual(
            self.mocked_created_at, object.updated_at + timezone.timedelta(days=0)
        )

    def test_updated_at_and_created_at_must_be_equals(self):
        qs = MacAddress.objects.all()
        for c in qs:
            self.assertEqual(c.created_at, c.updated_at)

    def test_updated_at_after_update(self):
        object = MacAddress.objects.order_by("id")[0]
        object.address = "66-66-66-66-66-66"
        object.save()

        self.assertLess(object.created_at, object.updated_at)

    # def test_get_absolute_url(self):
    #     object = MacAddress.objects.filter(
    #         address__exact="00-00-00-00-00-00")[0]

    #     self.assertEqual(
    #         object.get_absolute_url(), reverse("mac_address:list")
    #     )
