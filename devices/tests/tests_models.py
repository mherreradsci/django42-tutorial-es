from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from devices.models import Device

"""
Automated Test for Devices Model
"""


class DeviceTestCase(TestCase):
    # fixtures = ["init_devices.json"]

    @classmethod
    def setUpTestData(cls):
        """
        setUpTestData
        """

        cls.number_of_devices = 15
        cls.mocked_created_at = timezone.now()
        # created_at and updated_at must have the same datetime when the recors
        # are created
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=cls.mocked_created_at)
        ):
            for id in range(0, cls.number_of_devices):
                Device.objects.create(
                    code="DV" + str(id).zfill(4), name="Cliente " + str(id).zfill(4)
                )

    def test_string_representation(self):
        object = Device.objects.first()
        self.assertEqual(str(object), f"[{object.code}] {object.name}")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Device._meta.verbose_name_plural), "devices")

    def test_query_set_exists(self):
        qs = Device.objects.all()
        self.assertTrue(qs.exists())

    def test_query_counts(self):
        qs = Device.objects.all()
        self.assertEqual(qs.count(), self.number_of_devices)

    def test_validate_created_at(self):
        object = Device.objects.filter(code__exact="DV0000")[0]

        self.assertEqual(
            self.mocked_created_at, object.created_at + timezone.timedelta(days=0)
        )

    def test_updated_at(self):
        object = Device.objects.order_by("id").last()
        self.assertEqual(
            self.mocked_created_at, object.updated_at + timezone.timedelta(days=0)
        )

    def test_updated_at_and_created_at_must_be_equals(self):
        qs = Device.objects.all()
        for c in qs:
            self.assertEqual(c.created_at, c.updated_at)

    def test_updated_at_after_update(self):
        object = Device.objects.order_by("id")[0]
        object.name = "New name"
        object.save()

        self.assertLess(object.created_at, object.updated_at)

    def test_get_absolute_url(self):
        object = Device.objects.filter(code__exact="DV0000")[0]

        self.assertEqual(object.get_absolute_url(), reverse("devices:list"))

    def test_get_macaddress(self):
        object = Device.objects.filter(code__exact="DV0000")[0]
        self.assertEqual(object.get_macaddress().count(), 0)

    def test_natural_key(self):
        object = Device.objects.filter(code__exact="DV0000")[0]
        self.assertEqual(object.natural_key(), "DV0000")

    def test_get_by_natural_key(self):
        device = Device.objects.get_by_natural_key(code="DV0000")
        self.assertEqual(device.id, 1)
