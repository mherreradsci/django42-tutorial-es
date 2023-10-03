from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from customers.models import Customer
from devices.models import Device, DeviCustAssignment
from devices_assignments.forms import DeviCustAssignmentFormset


class DeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.user.save()

        # Create Devicers
        cls.number_of_devices = 2

        for id in range(0, cls.number_of_devices):
            Device.objects.create(
                code="DE" + str(id).zfill(4), name="Device " + str(id).zfill(4)
            )

        # Create Customers

        cls.number_of_customers = 2

        for id in range(0, cls.number_of_customers):
            Customer.objects.create(
                code="CU" + str(id).zfill(4), name="Customer " + str(id).zfill(4)
            )

        cls.first_device = Device.objects.order_by("id").first()
        cls.first_customer = Customer.objects.order_by("id").first()

        # Create Device Assignments
        cls.dca = DeviCustAssignment.objects.create(
            customer=cls.first_customer,
            device=cls.first_device,
            created_by=cls.user,
            updated_by=cls.user,
        )
        cls.dca.save()

    def test_device_update_view_formset_create(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        customer = Customer.objects.get(pk=2)
        url = reverse("devices_assignments:update", kwargs={"pk": customer.pk})

        response = self.client.get(path=url, follow=True)

        form_data = {
            "code": customer.code,
            "name": customer.name,
            "assignments-TOTAL_FORMS": 1,
            "assignments-INITIAL_FORMS": 0,
            "assignments-MAX_NUM_FORMS": 1000,
            "assignments-0-device": self.first_device.id,
            "assignments-0-active_from": timezone.now(),
            "assignments-0-active_until": timezone.now(),
            "assignments-0-created_by": "",
            "assignments-0-updated_by": "",
            "assignments-0-id": "",
        }

        formset = DeviCustAssignmentFormset(
            form_data, instance=self.first_customer, prefix="assignments"
        )

        self.assertEqual(formset.is_valid(), True)

        # test in case of save
        form_data["_save"] = "on"
        response = self.client.post(path=url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # self.assertRedirects(response, "/accounts/login/?next=/download/")

        d = DeviCustAssignment.objects.get(device=self.first_device, customer=customer)

        self.assertEqual(d.id, 2)

        self.assertEqual(self.user, d.created_by)

    def test_device_update_view_formset_update(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse(
            "devices_assignments:update", kwargs={"pk": self.first_customer.pk}
        )

        response = self.client.get(path=url, follow=True)

        form_data = {
            "code": self.first_customer.code,
            "name": self.first_customer.name,
            "assignments-TOTAL_FORMS": 1,
            "assignments-INITIAL_FORMS": 1,
            "assignments-MAX_NUM_FORMS": 1000,
            "assignments-0-device": self.first_device.id,
            "assignments-0-active_from": timezone.now(),
            "assignments-0-active_until": timezone.now(),
            "assignments-0-created_by": self.user,
            "assignments-0-updated_by": self.user,
            "assignments-0-id": str(self.dca.id),
        }

        formset = DeviCustAssignmentFormset(
            form_data, instance=self.first_customer, prefix="assignments"
        )

        self.assertEqual(formset.is_valid(), True)

        # test in case of _continue
        form_data["_continue"] = "on"

        response = self.client.post(path=url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        response.request.keys()

        d = DeviCustAssignment.objects.get(
            device=self.first_device, customer=self.first_customer
        )

        self.assertFalse(d.active)

    def test_device_update_view_form_invalid(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        form_data = {
            "code": self.first_customer.code,
            "name": self.first_customer.name,
            "assignments-TOTAL_FORMS": 1,
            "assignments-INITIAL_FORMS": 1,
            "assignments-MAX_NUM_FORMS": 1000,
            "assignments-0-device": "",
            "assignments-0-active_from": "2500-01-01 00:00:00",
            "assignments-0-active_until": "2500-01-01 00:00:00",
            "assignments-0-id": str(self.dca.id),
        }

        formset = DeviCustAssignmentFormset(
            form_data, instance=self.first_customer, prefix="assignments"
        )

        self.assertFalse(formset.is_valid())
        self.assertEqual(formset.total_error_count(), 2)

        self.assertIn(
            "This field is required.",
            str(formset[0].errors["device"]),
        )

        self.assertEqual(
            formset.errors[0]["active_until"][0],
            "active_until must be less or equal to active_from",
        )

        # Test View
        url = reverse(
            "devices_assignments:update", kwargs={"pk": self.first_customer.pk}
        )

        response = self.client.post(path=url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_device_update_view_formset_delete(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse(
            "devices_assignments:update", kwargs={"pk": self.first_customer.pk}
        )

        response = self.client.get(path=url, follow=True)
        self.assertEqual(response.status_code, 200)

        form_data = {
            "code": self.first_customer.code,
            "name": self.first_customer.name,
            "assignments-TOTAL_FORMS": 1,
            "assignments-INITIAL_FORMS": 1,
            "assignments-MAX_NUM_FORMS": 1000,
            "assignments-0-device": self.first_device,
            "assignments-0-active_from": timezone.now(),
            "assignments-0-active_until": timezone.now(),
            "assignments-0-created_by": "",
            "assignments-0-updated_by": "",
            "assignments-0-id": "1",
            "assignments-0-DELETE": True,
        }

        formset = DeviCustAssignmentFormset(
            form_data, instance=self.first_customer, prefix="assignments"
        )

        self.assertEqual(formset.is_valid(), True)

        response = self.client.post(path=url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        count = DeviCustAssignment.objects.filter(
            device=self.first_device, customer=self.first_customer
        ).count()

        self.assertEqual(count, 0)
