from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from devices.models import Device
from mac_address_types.models import MacAddressType
from devices.forms import DeviceMacAddressFormset


class DeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.user.save()

        cls.number_of_devices = 0

        for id in range(0, cls.number_of_devices):
            Device.objects.create(
                code="DE" + str(id).zfill(4), name="Device " + str(id).zfill(4)
            )

        cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
        cls.mac_address_type.save()

    def test_device_create_view_form_valid_success(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse("devices:create")

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

        form_data = {
            "code": "XXX",
            "name": "New Device",
            "active": True,
            "active_from": timezone.now(),
            "active_until": timezone.now(),
            "macaddress_set-TOTAL_FORMS": "0",
            "macaddress_set-INITIAL_FORMS": "0",
            "macaddress_set-MIN_NUM_FORMS": "0",
            "macaddress_set-MAX_NUM_FORMS": "0",
        }

        response = self.client.post(path=url, data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Device.objects.order_by("id").last().name, "New Device")

    def test_device_create_view_form_valid_error(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse("devices:create")

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

        form_data = {
            "code": "XXX",
            "name": "New Device",
            "active": True,
            "active_from": timezone.now(),
            "active_until": timezone.now(),
            "macaddress_set-TOTAL_FORMS": "0",
            # "macaddress_set-INITIAL_FORMS": "0",
            # "macaddress_set-MIN_NUM_FORMS": "0",
            # "macaddress_set-MAX_NUM_FORMS": "0",
        }

        formset = DeviceMacAddressFormset(form_data)

        self.assertFalse(formset.is_valid())

        response = self.client.post(path=url, data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
