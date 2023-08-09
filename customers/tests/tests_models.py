from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from unittest import mock

from customers.models import Customer
from accounts.models import User

"""
Automated Test for Customers Model
"""


class CustomerTestCase(TestCase):
    # fixtures = ["init_customers.json"]
    def setUp(self):
        """
        Setup
        """
        User.objects.create(username="init")
        self.number_of_customers = 50
        self.mocked_created_at = timezone.now()
        # created_at and updated_at must have the same datetime when the recors
        # are created
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=self.mocked_created_at)
        ):
            for id in range(0, self.number_of_customers):
                Customer.objects.create(
                    code="CR" + str(id).zfill(4), name="Cliente " + str(id).zfill(4)
                )

    def test_string_representation(self):
        object = Customer.objects.first()
        self.assertEqual(str(object), object.code)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Customer._meta.verbose_name_plural), "customers")

    def test_query_set_exists(self):
        qs = Customer.objects.all()
        self.assertTrue(qs.exists())

    def test_query_counts(self):
        qs = Customer.objects.all()
        self.assertEqual(qs.count(), self.number_of_customers)

    def test_validate_created_at(self):
        object = Customer.objects.filter(code__exact="CR0000")[0]

        self.assertEqual(
            self.mocked_created_at, object.created_at + timezone.timedelta(days=0)
        )

    def test_updated_at(self):
        object = Customer.objects.order_by("id").last()
        self.assertEqual(
            self.mocked_created_at, object.updated_at + timezone.timedelta(days=0)
        )

    def test_updated_at_and_created_at_must_be_equals(self):
        qs = Customer.objects.all()
        for c in qs:
            self.assertEqual(c.created_at, c.updated_at)

    def test_updated_at_after_update(self):
        object = Customer.objects.order_by("id")[0]
        object.name = "New name"
        object.save()

        self.assertLess(object.created_at, object.updated_at)

    def test_get_absolute_url(self):
        object = Customer.objects.filter(code__exact="CR0000")[0]

        self.assertEqual(object.get_absolute_url(), reverse("customers:list"))
