import copy

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from accounts.models import User
from devices.admin import DeviceAdmin
from devices.forms import DeviceMacAddressFormset
from devices.models import Device
from mac_address_types.models import MacAddressType
from mac_addresses.models import MacAddress


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


trace_on = False


def trace(device):
    if trace_on:
        print(
            f"[{str(device.id).ljust(5)}]"
            + f" [{device.name.ljust(30)}]"
            + f" [{str(device.created_by).ljust(10)}]"
            + f" [{str(device.created_at).ljust(32)}]"
            + f" [{str(device.updated_by).ljust(10)}]"
            + f" [{str(device.updated_at).ljust(32)}]"
        )


class DeviceAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password")

        cls.device = Device.objects.create(
            code="DEV001",
            name="Device 001",
        )

        cls.maad_type = MacAddressType.objects.create(code="MAT1", name="MAT1 Name")

    def test_device_admin_save_and_update_model(self):
        if trace_on:
            print(
                "id".ljust(5 + 3)
                + "name".ljust(30 + 3)
                + "created_by".ljust(10 + 3)
                + "created_at".ljust(32 + 3)
                + "updated_by".ljust(10 + 3)
                + "updated_at".ljust(32 + 3)
            )
        my_model_admin = DeviceAdmin(model=Device, admin_site=AdminSite())
        self.assertEqual(str(my_model_admin), "devices.DeviceAdmin")

        device = Device(code="DeviceX", name="Nombre DeviceX")
        trace(device)

        request = MockRequest()
        request.user = self.user

        my_model_admin.save_model(obj=device, request=request, form=None, change=False)
        trace(device)
        self.assertTrue(device.created_by, self.user)
        self.assertTrue(device.updated_by, self.user)

        device_copy = copy.deepcopy(device)
        device_copy.name = device.name + " updated"
        # trace(device)
        my_model_admin.save_model(
            obj=device_copy, request=request, form=None, change=True
        )
        trace(device)

        self.assertLess(device.created_at, device.updated_at)
        self.assertNotEqual(device_copy.name, device.name)

        # Test DeviceAdmin active
        self.assertEqual(my_model_admin.active(device), True)

        device.active_from = device.active_until
        self.assertEqual(my_model_admin.active(device), False)

    def test_model_admin_save_formset_create(self):
        data = {
            "macaddress_set-TOTAL_FORMS": 1,
            "macaddress_set-INITIAL_FORMS": 0,
            "macaddress_set-MAX_NUM_FORMS": 1000,
            "macaddress_set-0-address": "11-11-11-11-11-11",
            "macaddress_set-0-maad_type": self.maad_type,
            "macaddress_set-0-created_by": self.user,
            "macaddress_set-0-updated_by": self.user,
            "macaddress_set-0-id": "",
        }
        formset = DeviceMacAddressFormset(data, instance=self.device)

        self.assertEqual(formset.is_valid(), True)

        my_model_admin = DeviceAdmin(model=Device, admin_site=AdminSite())
        request = MockRequest()
        request.user = self.user

        my_model_admin.save_formset(request, form=None, formset=formset, change=True)
        qs = MacAddress.objects.filter(device=self.device)

        count = qs.count()

        self.assertEqual(count, 1)
