from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

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

        cls.ma = MacAddress.objects.create(
            address="00-00-00-00-00-00",
            maad_type=cls.mac_address_type,
            device=cls.first_device,
        )
        cls.ma.save()

        cls.ma_count = MacAddress.objects.count()

    def test_device_update_view_with_formset(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = Device.objects.order_by("id").first()

        url = reverse("devices:update", kwargs={"pk": object.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse("devices:update", kwargs={"pk": object.pk})
        form_data = {
            "code": object.code,
            "name": object.name,
            "active": object.active,
            "active_from": object.active_from,
            "active_until": object.active_until,
            "created_by": self.user,
            "updated_by": self.user,
            "macaddress_set-TOTAL_FORMS": "1",
            "macaddress_set-INITIAL_FORMS": "1",
            "macaddress_set-MIN_NUM_FORMS": "0",
            "macaddress_set-MAX_NUM_FORMS": "",
            "macaddress_set-0-address": "11-11-11-11-11-11",
            "macaddress_set-0-maad_type": "1",  # self.ma.maad_type,
            "macaddress_set-0-active": "1",
            "macaddress_set-0-active_from": timezone.now(),
            "macaddress_set-0-active_until": timezone.now(),
            "macaddress_set-0-created_by": self.user,
            "macaddress_set-0-updated_by": self.user,
            "macaddress_set-0-id": "1",
        }
        formset = DeviceMacAddressFormset(form_data)

        self.assertTrue(formset.is_valid())

        response = self.client.post(path=url, data=form_data)
        self.assertEqual(response.status_code, 302)

        self.ma.refresh_from_db()

        ma_count = MacAddress.objects.count()

        self.assertEqual(ma_count, 1)

        self.assertEqual(self.ma.address, "11-11-11-11-11-11")

        self.assertEqual(response.url, reverse("devices:list"))
