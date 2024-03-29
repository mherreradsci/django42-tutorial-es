from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from mac_address_types.models import MacAddressType

"""
Automated Test for MacAddressType Model
"""


class MacAddressTypeTestCase(TestCase):
    """
    MacAddressType Test Case
    """

    @classmethod
    def setUpTestData(cls):
        """
        setUpTestData
        """
        User.objects.create(username="init")
        cls.number_of_mac_address_types = 15
        cls.mocked_created_at = timezone.now()
        # created_at and updated_at must have the same datetime when the recors
        # are created
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=cls.mocked_created_at)
        ):
            for id in range(0, cls.number_of_mac_address_types):
                MacAddressType.objects.create(
                    code="MC" + str(id).zfill(4),
                    name="MAC Address Type" + str(id).zfill(4),
                )

    def test_string_representation(self):
        object = MacAddressType.objects.first()
        self.assertEqual(str(object), f"[{object.code}] {object.desc}")

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(MacAddressType._meta.verbose_name_plural), "MAC Address Types"
        )

    def test_query_set_exists(self):
        qs = MacAddressType.objects.all()
        self.assertTrue(qs.exists())

    def test_query_counts(self):
        qs = MacAddressType.objects.all()
        self.assertEqual(qs.count(), self.number_of_mac_address_types)

    def test_validate_created_at(self):
        object = MacAddressType.objects.filter(code__exact="MC0000")[0]

        self.assertEqual(
            self.mocked_created_at, object.created_at + timezone.timedelta(days=0)
        )

    def test_updated_at(self):
        object = MacAddressType.objects.order_by("id").last()
        self.assertEqual(
            self.mocked_created_at, object.updated_at + timezone.timedelta(days=0)
        )

    def test_updated_at_and_created_at_must_be_equals(self):
        qs = MacAddressType.objects.all()
        for c in qs:
            self.assertEqual(c.created_at, c.updated_at)

    def test_updated_at_after_update(self):
        object = MacAddressType.objects.order_by("id")[0]
        object.name = "New name"
        object.save()

        self.assertLess(object.created_at, object.updated_at)

    def test_get_absolute_url(self):
        object = MacAddressType.objects.filter(code__exact="MC0000")[0]

        self.assertEqual(object.get_absolute_url(), reverse("mac_address_types:list"))
