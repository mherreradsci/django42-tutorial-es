from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from accounts.models import User
from devices.forms import DeviceMacAddressFormset
from devices.models import Device
from mac_address_types.models import MacAddressType
from mac_addresses.models import MacAddress


class DeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.user.save()

        cls.number_of_devices = 15

        for id in range(0, cls.number_of_devices):
            Device.objects.create(
                code="DE" + str(id).zfill(4), name="Device " + str(id).zfill(4)
            )

        cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
        cls.mac_address_type.save()

        cls.first_device = Device.objects.order_by("id").first()

        cls.ma_count = MacAddress.objects.count()

    def test_device_create_view(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse("devices:create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, MacAddress.objects.count())

        form_data = {
            "code": "123456",
            "macaddress_set-TOTAL_FORMS": "1",
            "macaddress_set-INITIAL_FORMS": "0",
            "macaddress_set-MIN_NUM_FORMS": "0",
            "macaddress_set-MAX_NUM_FORMS": "",
            "macaddress_set-0-address": "NEW MAC ADDRESS02",
            "macaddress_set-0-maad_type": "1",
            "macaddress_set-0-DELETE": False,
        }
        formset = DeviceMacAddressFormset(form_data)

        self.assertTrue(formset.is_valid())

        response = self.client.post(path=url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        de = Device.objects.order_by("id").last()
        self.assertEqual(de.code, "123456")

        ma_count = MacAddress.objects.count()

        self.assertEqual(ma_count, 1)

        self.assertRedirects(response, reverse("devices:list"))
