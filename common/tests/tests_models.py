from django.test import TestCase

from customers.models import Customer

"""
Automated Test for Common Model
"""
from django.core.exceptions import ValidationError


class ValidityInfoTestCase(TestCase):
    def test_validate_active_from_not_null(self):
        customer = Customer.objects.create(code="CR0000")
        customer.active_from = None
        with self.assertRaises(ValidationError):
            customer.clean()
        # the same writed in other way
        self.assertRaises(ValidationError, customer.clean)

        try:
            customer.clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("active_from"))
            self.assertEqual(
                e.message_dict["active_from"], ["active_from without value"]
            )

        with self.assertRaisesRegex(ValidationError, "active_from without value"):
            customer.clean()

    def test_validate_active_until_not_null(self):
        customer = Customer.objects.create(
            code="CR0000",
        )
        customer.active_until = None
        try:
            customer.clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("active_until"))
            self.assertEqual(
                e.message_dict["active_until"], ["active_until without value"]
            )

    def test_validate_active_from_must_greater_than_active_until(self):
        customer = Customer.objects.create(code="CR0000")
        customer.active_until = customer.active_from
        try:
            customer.clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("active_until"))
            self.assertEqual(
                e.message_dict["active_until"],
                ["active_until must be less or equal to active_from"],
            )
